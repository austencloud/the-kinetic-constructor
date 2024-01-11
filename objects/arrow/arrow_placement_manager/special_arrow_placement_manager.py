from collections import OrderedDict
import json
import re
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Union
from constants import BLUE, LEADING, RED, TRAILING

from objects.arrow.arrow import Arrow
from utilities.TypeChecking.Letters import (
    Type1_hybrid_letters,
    Type1_letters,
    Type1_non_hybrid_letters,
    Type2_letters,
    non_hybrid_letters,
)


if TYPE_CHECKING:
    from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
        MainArrowPlacementManager,
    )
    from objects.pictograph.pictograph import Pictograph


class SpecialArrowPlacementManager:
    def __init__(
        self,
        pictograph: "Pictograph",
        main_arrow_placement_manager: "MainArrowPlacementManager",
    ):
        self.pictograph = pictograph
        self.main_arrow_placement_manager = main_arrow_placement_manager
        self.blue_arrow = self.pictograph.arrows.get(BLUE)
        self.red_arrow = self.pictograph.arrows.get(RED)
        self.json_path = "arrow_placement/special_placements.json"
        self.data_modified = False  # Flag to track if data has been modified
        self.special_placements = self._load_placements()

    def add_and_sort_new_entry(
        self, letter: str, adjustment_key: str, new_adjustment: Dict
    ):
        letter_data = self.special_placements.get(letter, {})

        if adjustment_key not in letter_data:
            letter_data[adjustment_key] = new_adjustment
            # letter_data = self._sort_entries(letter_data)
            self.special_placements[letter] = letter_data
            self.data_modified = True

    def update_adjustment(self, letter: str, adjustment_key: str, new_adjustment: Dict):
        self.special_placements[letter][adjustment_key] = new_adjustment
        self.data_modified = True

    def update_specific_placement(self, letter: str, adjustment_key: str, new_adjustment: Dict) -> None:
        """Update a specific placement in the JSON file."""
        # Load the current placements from the file
        with open(self.json_path, "r") as file:
            data = json.load(file)

        # Update only the relevant entry
        if letter in data:
            if adjustment_key in data[letter]:
                data[letter][adjustment_key].update(new_adjustment)
            else:
                data[letter][adjustment_key] = new_adjustment
        else:
            data[letter] = {adjustment_key: new_adjustment}

        # Write the updated data back to the file
        with open(self.json_path, "w") as file:
            json.dump(data, file, indent=2)
            
    def _load_placements(self) -> Dict[str, Dict[str, Tuple[int, int]]]:
        with open(self.json_path, "r") as file:
            data = json.load(file)

        if self.data_modified:
            with open(self.json_path, "w") as file:
                json_str = json.dumps(data, indent=2)
                compact_json_str = re.sub(
                    r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
                )
                file.write(compact_json_str)
            self.data_modified = False  # Reset the flag after writing

        return data

    def _sort_entries(self, letter_data: Dict[str, Tuple[int, int]]) -> Dict:
        def sort_key(item) -> Tuple[int, Union[int, float], Union[int, float]]:
            key = item[0]
            numbers = [
                float(num) if "." in num else int(num)
                for num in re.findall(r"\d+\.?\d*", key)
            ]
            char = re.search(r"[so]", key)

            if self.pictograph.letter in Type1_letters:
                return (numbers[0], numbers[1] if len(numbers) > 1 else float("inf"))
            elif char:
                char_priority = {"s": 1, "o": 2}.get(char.group(), 3)
                return (
                    char_priority,
                    numbers[0],
                    numbers[1] if len(numbers) > 1 else float("inf"),
                )
            else:
                return (0, numbers[0], numbers[1] if len(numbers) > 1 else float("inf"))

        return dict(sorted(letter_data.items(), key=sort_key))

    def get_rotation_angle_override(self, arrow: Arrow) -> Optional[int]:
        adjustment_key = self._generate_adjustment_key(arrow)
        letter_adjustments = self.special_placements.get(
            self.pictograph.letter, {}
        ).get(adjustment_key, {})
        return letter_adjustments.get(f"{arrow.motion_type}_rot_angle", {})

    def _generate_adjustment_key(self, arrow: Arrow) -> str:
        letter = self.pictograph.letter
        if letter in ["S", "T"]:
            leading_motion = self.pictograph.get_leading_motion()
            following_motion = (
                self.blue_arrow.motion
                if leading_motion == self.red_arrow.motion
                else self.red_arrow.motion
            )
            return f"({leading_motion.turns}, {following_motion.turns})"

        elif letter in Type1_hybrid_letters:
            (
                pro_arrow,
                anti_arrow,
            ) = self.main_arrow_placement_manager._get_pro_anti_arrows()
            return f"({pro_arrow.turns}, {anti_arrow.turns})"

        elif letter in Type1_non_hybrid_letters:
            blue_arrow = self.pictograph.arrows.get(BLUE)
            red_arrow = self.pictograph.arrows.get(RED)
            return f"({blue_arrow.turns}, {red_arrow.turns})"

        elif letter in Type2_letters:
            shift_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_shift()
                else self.pictograph.blue_motion
            )
            static_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_static()
                else self.pictograph.blue_motion
            )

            if static_motion.turns > 0:
                if static_motion.turns in [0.0, 1.0, 2.0, 3.0]:
                    static_motion.turns = int(static_motion.turns)

                if static_motion.prop_rot_dir and shift_motion.prop_rot_dir:
                    if static_motion.prop_rot_dir != shift_motion.prop_rot_dir:
                        direction = "opp"
                    elif static_motion.prop_rot_dir == shift_motion.prop_rot_dir:
                        direction = "same"

                    direction_prefix = direction[0]
                    adjustment_key_str = f"({direction_prefix}, {shift_motion.turns}, {static_motion.turns})"
                # elif either of the values are None
                else:
                    adjustment_key_str = None
            elif static_motion.turns == 0:
                adjustment_key_str = f"({shift_motion.turns}, {static_motion.turns})"
            return adjustment_key_str

        else:
            return f"({arrow.turns}, {arrow.motion_type})"

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        self.special_placements = self._load_placements()
        letter_adjustments = self.special_placements.get(letter, {}).get(
            adjustment_key, {}
        )
        if letter in ["S", "T"]:
            leading_motion = self.pictograph.get_leading_motion()
            trailing_motion = (
                self.blue_arrow.motion
                if leading_motion == self.red_arrow.motion
                else self.red_arrow.motion
            )
            leading_motion.arrow.lead_state = LEADING
            trailing_motion.arrow.lead_state = TRAILING

            return letter_adjustments.get(arrow.lead_state)
        elif letter in Type1_hybrid_letters:
            return letter_adjustments.get(arrow.motion_type)
        elif letter in non_hybrid_letters:
            return letter_adjustments.get(arrow.color)
        elif letter in Type2_letters:
            shift_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_shift()
                else self.pictograph.blue_motion
            )
            static_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_static()
                else self.pictograph.blue_motion
            )

            if static_motion.turns > 0:
                if static_motion.prop_rot_dir != shift_motion.prop_rot_dir:
                    direction = "opp"
                elif static_motion.prop_rot_dir == shift_motion.prop_rot_dir:
                    direction = "same"

                direction_prefix = direction[0]
                adjustment_key_str = (
                    f"({direction_prefix}, {shift_motion.turns}, {static_motion.turns})"
                )
            elif static_motion.turns == 0:
                adjustment_key_str = f"({shift_motion.turns}, {static_motion.turns})"
            letter_adjustments = self.special_placements.get(
                self.pictograph.letter, {}
            ).get(adjustment_key_str, {})
            if arrow.motion.is_static():
                return letter_adjustments.get(static_motion.motion_type, {})
            elif arrow.motion.is_shift():
                return letter_adjustments.get(shift_motion.motion_type, {})
        return None

    def _get_special_adjustment(
        self, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        letter_adjustments = self.special_placements.get(
            self.pictograph.letter, {}
        ).get(adjustment_key, {})

        if (
            self.pictograph.letter in Type1_hybrid_letters
            or self.pictograph.letter in Type2_letters
        ):
            return letter_adjustments.get(arrow.motion_type)
        elif self.pictograph.letter in Type1_non_hybrid_letters:
            return letter_adjustments.get(arrow.color)

        return None

    def _convert_key_to_tuple(self, key: str) -> Tuple[int, int]:
        key_values = key.strip("()").split(", ")
        converted_values = []
        for value in key_values:
            if value.isdigit() and int(value) in [0, 1, 2, 3]:
                converted_values.append(int(value))
            else:
                converted_values.append(float(value))
        return tuple(converted_values)
