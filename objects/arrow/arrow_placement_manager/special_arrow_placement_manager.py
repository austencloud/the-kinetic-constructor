from collections import OrderedDict
import json
import re
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Union

from numpy import place
from constants import BLUE, LEADING, PRO, RED, TRAILING

from objects.arrow.arrow import Arrow
from utilities.TypeChecking.Letters import (
    Type1_hybrid_letters,
    Type1_letters,
    Type1_non_hybrid_letters,
    Type2_letters,
    Type3_letters,
    non_hybrid_letters,
)


if TYPE_CHECKING:
    from objects.arrow.arrow_placement_manager.main_arrow_placement_manager import (
        MainArrowPlacementManager,
    )
    from objects.pictograph.pictograph import Pictograph


class SpecialArrowPlacementManager:
    def __init__(
        self, pictograph: "Pictograph", main_manager: "MainArrowPlacementManager"
    ):
        self.pictograph = pictograph
        self.main_manager = main_manager
        self.json_path = "arrow_placement/special_placements.json"
        self.special_placements = None
        self.data_modified = False

    def _load_placements(self) -> Dict:
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                self.special_placements = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")
            self.special_placements = {}
        return self.special_placements

    def update_specific_entry_in_json(
        self, letter: str, adjustment_key: str, new_data: Dict
    ) -> None:
        """Update a specific entry in the JSON file.

        Args:
            letter
            adjustment_key
            new_data
        """
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            letter_data = data.get(letter, {})
            letter_data[adjustment_key] = new_data
            data[letter] = letter_data
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            formatted_json_str = re.sub(
                r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", json_str
            )
            with open(self.json_path, "w", encoding="utf-8") as file:
                file.write(formatted_json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")

    def add_and_sort_new_entry(
        self, letter: str, adjustment_key: str, new_adjustment: Dict
    ) -> None:
        letter_data = self.special_placements.get(letter, {})

        if adjustment_key not in letter_data:
            letter_data[adjustment_key] = new_adjustment
            self.special_placements[letter] = letter_data
            self.data_modified = True

    def update_arrow_adjustments_in_json(
        self, adjustment: Tuple[int, int], arrow: "Arrow"
    ) -> None:
        """Updates the arrow adjustments in the JSON file."""
        if not arrow:
            return

        # Load current placements
        self._load_placements()

        adjustment_key = self._generate_adjustment_key(arrow)
        letter_data: Dict = self.special_placements.get(self.pictograph.letter, {})
        turn_data = letter_data.get(adjustment_key, {})

        if turn_data:
            self._update_turn_data(turn_data, arrow, adjustment)
        else:
            turn_data = self._create_default_turn_data(arrow, adjustment)

        # Update the specific entry in the JSON file
        self.update_specific_entry_in_json(
            self.pictograph.letter, adjustment_key, turn_data
        )

    def _update_turn_data(
        self, turn_data: Dict, arrow: "Arrow", adjustment: Tuple[int, int]
    ) -> None:
        key = self._determine_key(arrow)
        turn_data.setdefault(key, self._get_default_data(arrow))
        turn_data[key] = [
            turn_data[key][0] + adjustment[0],
            turn_data[key][1] + adjustment[1],
        ]

    def _get_default_data(self, arrow: "Arrow") -> Tuple[int, int]:
        default_mgr = self.pictograph.arrow_placement_manager.default_manager
        default_turn_data = default_mgr.get_default_adjustment(arrow)
        return (default_turn_data[0], default_turn_data[1])

    def _create_default_turn_data(
        self, arrow: "Arrow", adjustment: Tuple[int, int]
    ) -> Dict:
        default_mgr = self.pictograph.arrow_placement_manager.default_manager
        default_turn_data = default_mgr.get_default_adjustment(arrow)
        other_arrow_default_turn_data = default_mgr.get_default_adjustment(
            self.pictograph.blue_arrow
            if arrow == self.pictograph.red_arrow
            else self.pictograph.red_arrow
        )
        key = self._determine_key(arrow)

        return {
            key: [
                default_turn_data[0] + adjustment[0],
                default_turn_data[1] + adjustment[1],
            ]
        }

    def _determine_key(self, arrow: "Arrow") -> str:
        if self.pictograph.letter in ["S", "T"]:
            return arrow.lead_state
        elif self.pictograph.letter in Type1_non_hybrid_letters:
            return arrow.color
        else:
            return arrow.motion_type

    def _get_other_key(self, arrow: "Arrow") -> str:
        other_arrow = (
            self.pictograph.blue_arrow
            if arrow == self.pictograph.red_arrow
            else self.pictograph.red_arrow
        )
        if self.pictograph.letter in ["S", "T"]:
            return other_arrow.lead_state
        elif self.pictograph.letter in Type1_non_hybrid_letters:
            return other_arrow.color
        else:
            return other_arrow.motion_type

    def _sort_entries(self, letter_data: Dict[str, Tuple[int, int]]) -> Dict:
        """Should use this occasionally to sort the entries in the JSON file."""

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

    def get_rot_angle_override(self, arrow: Arrow) -> Optional[int]:
        adjustment_key = self._generate_adjustment_key(arrow)
        placements = self._load_placements()
        letter_adjustments = placements.get(self.pictograph.letter, {}).get(
            adjustment_key, {}
        )
        return letter_adjustments.get(f"{arrow.motion_type}_rot_angle", {})

    def _generate_adjustment_key(self, arrow: Arrow) -> str:
        letter = self.pictograph.letter
        if letter in ["S", "T"]:
            leading_motion = self.pictograph.get_leading_motion()
            following_motion = (
                self.pictograph.blue_arrow.motion
                if leading_motion == self.pictograph.red_arrow.motion
                else self.pictograph.red_arrow.motion
            )
            return f"({leading_motion.turns}, {following_motion.turns})"

        elif letter in Type1_hybrid_letters:
            pro_arrow = (
                self.pictograph.arrows[RED]
                if self.pictograph.arrows[RED].motion_type == PRO
                else self.pictograph.arrows[BLUE]
            )
            anti_arrow = (
                self.pictograph.arrows[RED]
                if self.pictograph.arrows[RED].motion_type == PRO
                else self.pictograph.arrows[BLUE]
            )
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
                self.pictograph.blue_arrow.motion
                if leading_motion == self.pictograph.red_arrow.motion
                else self.pictograph.red_arrow.motion
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
        
        elif letter in Type3_letters:
            shift_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_shift()
                else self.pictograph.blue_motion
            )
            dash_motion = (
                self.pictograph.red_motion
                if self.pictograph.red_motion.is_dash()
                else self.pictograph.blue_motion
            )

            if dash_motion.turns > 0:
                if dash_motion.prop_rot_dir != shift_motion.prop_rot_dir:
                    direction = "opp"
                elif dash_motion.prop_rot_dir == shift_motion.prop_rot_dir:
                    direction = "same"

                direction_prefix = direction[0]
                adjustment_key_str = (
                    f"({direction_prefix}, {shift_motion.turns}, {dash_motion.turns})"
                )
            elif dash_motion.turns == 0:
                adjustment_key_str = f"({shift_motion.turns}, {dash_motion.turns})"
            letter_adjustments = self.special_placements.get(
                self.pictograph.letter, {}
            ).get(adjustment_key_str, {})
            if arrow.motion.is_dash():
                return letter_adjustments.get(dash_motion.motion_type, {})
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