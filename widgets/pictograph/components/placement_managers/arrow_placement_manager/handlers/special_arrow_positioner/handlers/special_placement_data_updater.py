import json
import os
import re
from typing import TYPE_CHECKING, Dict, Tuple
from constants import CLOCK, COUNTER, IN, OUT

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
        # Determine the correct orientation key ('from_radial' or 'from_antiradial')
        orientation_key = (
            "from_radial" if arrow.motion.start_ori in [IN, OUT] else "from_antiradial"
        )

        # Access the correct placements data based on the orientation
        letter_data = (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                orientation_key
            ].get(letter, {})
        )

        turn_data = letter_data.get(turns_tuple, {})

        if turn_data:
            self._update_turn_data(turn_data, arrow, adjustment)
        else:
            turn_data = self._create_default_turn_data(arrow, adjustment)

        letter_data[turns_tuple] = turn_data
        self.positioner.placement_manager.pictograph.main_widget.special_placements[
            letter
        ] = letter_data
        self.update_specific_entry_in_json(letter, letter_data, arrow)

    def update_specific_entry_in_json(
        self, letter: Letters, letter_data: Dict, arrow: Arrow
    ) -> None:
        """Update a specific entry in the JSON file."""
        try:
            subfolder = (
                "from_radial"
                if arrow.motion.start_ori in [IN, OUT]
                else "from_antiradial"
            )
            base_directory = (
                self.positioner.placement_manager.pictograph.main_widget.parent_directory
            )

            # Construct the file path
            file_path = os.path.join(
                base_directory, subfolder, f"{letter}_placements.json"
            )

            # Check if the directory exists, if not, create it
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Check if the file exists. If not, initialize an empty dictionary for the letter
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump({letter: {}}, file, indent=2, ensure_ascii=False)

            # Now, read the existing data, update it, and write back
            with open(file_path, "r", encoding="utf-8") as file:
                existing_data = json.load(file)

            existing_data[letter] = letter_data

            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(
                    existing_data, indent=2, ensure_ascii=False
                )
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
        except Exception as e:
            print(f"Error occurred while updating JSON file: {e}")

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

    def remove_special_placement_entry(self, letter: str, arrow: "Arrow") -> None:
        """Remove a specific entry from the special placements JSON file."""
        # Determine the orientation key and file path
        orientation_key = (
            "from_radial" if arrow.motion.start_ori in [IN, OUT] else "from_antiradial"
        )
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )

        # Load current data
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data: Dict = json.load(file)
            letter_data = data.get(letter, {})

            # Remove the specific entry
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                letter
            )
            if turns_tuple in letter_data:
                del letter_data[turns_tuple]

            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)

        arrow.pictograph.main_widget.refresh_placements()
