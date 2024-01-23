import json
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
        """Updates the arrow adjustments in the JSON file."""
        if not arrow:
            return

        self.positioner.special_placements

        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
            arrow.scene.letter
        )
        letter_data: Dict = self.positioner.special_placements.get(
            self.positioner.pictograph.letter, {}
        )
        turn_data = letter_data.get(turns_tuple, {})

        if turn_data:
            self._update_turn_data(turn_data, arrow, adjustment)
        else:
            turn_data = self._create_default_turn_data(arrow, adjustment)

        self.update_specific_entry_in_json(
            self.positioner.pictograph.letter, turns_tuple, turn_data
        )

    def update_specific_entry_in_json(
        self, letter: Letters, turns_tuple: str, new_data: Dict
    ) -> None:
        """Update a specific entry in the JSON file."""
        try:
            with open(
                self.positioner.data_loader.json_path, "r", encoding="utf-8"
            ) as file:
                data: Dict = json.load(file)
            letter_data = data.get(letter, {})
            letter_data[turns_tuple] = new_data
            data[letter] = letter_data
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            formatted_json_str = re.sub(
                r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", json_str
            )
            with open(
                self.positioner.data_loader.json_path, "w", encoding="utf-8"
            ) as file:
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
