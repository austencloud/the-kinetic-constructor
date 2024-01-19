import json
import re
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Union

from .adjustment_key_generator import AdjustmentKeyGenerator
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type1_letters,
    Type1_non_hybrid_letters,
    Type2_letters,
    Type3_letters,
    non_hybrid_letters,
)

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager
    from widgets.pictograph.pictograph import Pictograph


class SpecialArrowPositioner:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.data_loader = SpecialPlacementDataLoader()
        self.data_updater = SpecialPlacementDataUpdater(pictograph)
        self.adjustment_calculator = AdjustmentCalculator(pictograph)
        self.key_generator = KeyGenerator(pictograph)
        self.rot_angle_handler = RotAngleOverrideHandler(pictograph)
        self.data_sorter = DataSorter(pictograph)
        self.adjustment_mapper = AdjustmentMapper(pictograph)
        self.special_placements: Dict = self.data_loader.load_placements()

    def update_arrow_placement(self, arrow: Arrow) -> None:
        adjustment_key = self.key_generator.generate_adjustment_key(arrow)
        adjustment = self.adjustment_calculator.calculate_adjustment(
            arrow, adjustment_key
        )
        if adjustment:
            self.data_updater.update_specific_entry(
                self.pictograph.letter, adjustment_key, adjustment
            )
            
    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, adjustment_key: str = None
    ) -> Optional[Tuple[int, int]]:
        if adjustment_key is None:
            adjustment_key = self.key_generator.determine_key(letter)
        self.special_placements: Dict[str, Dict] = self.data_loader.load_placements()
        letter_adjustments: Dict = self.special_placements.get(letter, {}).get(
            adjustment_key, {}
        )

        adjustment_map = {
            "S": letter_adjustments.get(arrow.motion.lead_state),
            "T": letter_adjustments.get(arrow.motion.lead_state),
            **{
                letter: letter_adjustments.get(arrow.motion_type)
                for letter in Type1_hybrid_letters
            },
            **{
                letter: letter_adjustments.get(arrow.color)
                for letter in non_hybrid_letters
            },
            **{
                letter: letter_adjustments.get(arrow.motion_type)
                for letter in Type2_letters + Type3_letters
            },
        }

        return adjustment_map.get(letter)

class SpecialPlacementDataLoader:
    def __init__(self) -> None:
        self.json_path = "arrow_placement/special_placements.json"

    def load_placements(self) -> Dict:
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File not found: {self.json_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")
            return {}


class SpecialPlacementDataUpdater:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.data_loader = SpecialPlacementDataLoader()

    def update_specific_entry(
        self, letter: str, adjustment_key: str, new_data: Dict
    ) -> None:
        data = self.data_loader.load_placements()
        data.setdefault(letter, {})[adjustment_key] = new_data
        with open(self.data_loader.json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


class AdjustmentCalculator:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.data_loader = SpecialPlacementDataLoader()
        self.key_generator = KeyGenerator(pictograph)

    def calculate_adjustment(
        self, arrow: Arrow, adjustment_key: str
    ) -> Optional[Tuple[int, int]]:
        placements = self.data_loader.load_placements()
        letter_data: Dict[str, Dict] = placements.get(self.pictograph.letter, {})
        return letter_data.get(adjustment_key, {}).get(
            self.key_generator.determine_key(arrow)
        )


class KeyGenerator:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def determine_key(self, arrow: "Arrow") -> str:
        if self.pictograph.letter in ["S", "T"]:
            return arrow.motion.lead_state
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
            return other_arrow.motion.lead_state
        elif self.pictograph.letter in Type1_non_hybrid_letters:
            return other_arrow.color
        else:
            return other_arrow.motion_type

    def generate_adjustment_key(self, arrow: Arrow) -> str:
        key = self.determine_key(arrow)
        other_key = self._get_other_key(arrow)
        return f"{key}({other_key})"


class RotAngleOverrideHandler:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.data_loader = SpecialPlacementDataLoader()

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = self.data_loader.load_placements()
        letter_data: Dict[str, Dict] = placements.get(self.pictograph.letter, {})
        adjustment_key = KeyGenerator(self.pictograph).generate_adjustment_key(arrow)
        return letter_data.get(adjustment_key, {}).get(f"{arrow.motion_type}_rot_angle")


class DataSorter:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.data_loader = SpecialPlacementDataLoader()
        self.data_updater = SpecialPlacementDataUpdater(pictograph)

    def sort_entries(self) -> None:
        data = self.data_loader.load_placements()
        for letter, letter_data in data.items():
            sorted_data = self._sort_letter_data(letter_data)
            data[letter] = sorted_data
        self.data_updater.update_specific_entry(data)

    def _sort_letter_data(self, letter_data: Dict) -> Dict:
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


class AdjustmentMapper:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.adjustment_calculator = AdjustmentCalculator(pictograph)

    def apply_adjustment_to_arrow(self, arrow: Arrow) -> None:
        key_generator = KeyGenerator(self.pictograph)
        adjustment_key = key_generator.generate_adjustment_key(arrow)
        adjustment = self.adjustment_calculator.calculate_adjustment(
            arrow, adjustment_key
        )

        if adjustment:
            self._apply_adjustment(arrow, adjustment)

    def _apply_adjustment(self, arrow: Arrow, adjustment: Tuple[int, int]) -> None:
        # Calculate the new position based on the adjustment
        new_x = arrow.x() + adjustment[0]
        new_y = arrow.y() + adjustment[1]
        # Apply the new position to the arrow
        arrow.setPos(new_x, new_y)
