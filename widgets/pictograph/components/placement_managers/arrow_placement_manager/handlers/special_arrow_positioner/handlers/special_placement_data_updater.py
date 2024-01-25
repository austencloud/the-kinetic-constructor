import json
import os
import re
from typing import TYPE_CHECKING, Dict, Tuple

from objects.arrow.arrow import Arrow
from utilities.TypeChecking.TypeChecking import Letters

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class SpecialPlacementDataUpdater:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def update_arrow_adjustments_in_json(
        self, adjustment: Tuple[int, int], arrow: "Arrow"
    ) -> None:
        if not arrow:
            return

        letter = self.positioner.pictograph.letter

        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        letter_data: Dict = self.positioner.placement_manager.pictograph.main_widget.load_special_placements().get(letter, {})
        turn_data = letter_data.get(turns_tuple, {})

        if turn_data:
            self._update_turn_data(turn_data, arrow, adjustment)
        else:
            turn_data = self._create_default_turn_data(arrow, adjustment)

        letter_data[turns_tuple] = turn_data
        self.positioner.placement_manager.pictograph.main_widget.special_placements[letter] = letter_data
        self.update_specific_entry_in_json(letter, letter_data)

    def update_specific_entry_in_json(self, letter: Letters, letter_data: Dict) -> None:
        """Update a specific entry in the JSON file."""
        try:
            file_path = os.path.join(
                self.positioner.placement_manager.pictograph.main_widget.directory, f"{letter}_placements.json"
            ) 
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(
                    {letter: letter_data}, indent=2, ensure_ascii=False
                )
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error occurred: {e}")

    def _update_turn_data(
        self, turn_data: Dict, arrow: "Arrow", adjustment: Tuple[int, int]
    ) -> None:
        key = self.positioner.motion_key_generator.generate_motion_key(arrow)
        turn_data.setdefault(key, self._get_default_data(arrow))
        turn_data[key] = [
            turn_data[key][0] + adjustment[0],
            turn_data[key][1] + adjustment[1],
        ]

    def _get_default_data(self, arrow: "Arrow") -> Tuple[int, int]:
        default_mgr = (
            self.positioner.pictograph.arrow_placement_manager.default_positioner
        )
        default_turn_data = default_mgr.get_default_adjustment(arrow)
        return (default_turn_data[0], default_turn_data[1])

    def _create_default_turn_data(
        self, arrow: "Arrow", adjustment: Tuple[int, int]
    ) -> Dict:
        default_mgr = (
            self.positioner.pictograph.arrow_placement_manager.default_positioner
        )
        default_turn_data = default_mgr.get_default_adjustment(arrow)
        key = self.positioner.motion_key_generator.generate_motion_key(arrow)
        return {
            key: [
                default_turn_data[0] + adjustment[0],
                default_turn_data[1] + adjustment[1],
            ]
        }
