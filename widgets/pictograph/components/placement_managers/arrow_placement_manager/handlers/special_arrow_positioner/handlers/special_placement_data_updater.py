import json
import os
import re
from typing import TYPE_CHECKING, Dict, Tuple, Union
from constants import CLOCK, COUNTER, IN, OUT

from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
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
        # Determine the correct orientation key ('from_radial' or 'from_nonradial')
        orientation_key = (
            "from_radial" if arrow.motion.start_ori in [IN, OUT] else "from_nonradial"
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
        self, letter: Letters, letter_data: Dict, object: Union[Arrow, Prop]
    ) -> None:
        """Update a specific entry in the JSON file."""

        try:
            # Determine the subfolder based on the object type
            if object.motion.start_ori in [IN, OUT]:
                subfolder = "from_radial"
            elif object.motion.start_ori in [CLOCK, COUNTER]:
                subfolder = "from_nonradial"


            base_directory = (
                self.positioner.placement_manager.pictograph.main_widget.parent_directory
            )

            # Construct the file path
            file_path = os.path.join(
                base_directory, subfolder, f"{letter}_placements.json"
            )

            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Load existing data or initialize an empty dictionary
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    existing_data = json.load(file)
            else:
                existing_data = {letter: {}}

            # Update the specific entry
            existing_data[letter] = letter_data

            # if isinstance(object, Prop):
            #     # Construct the override key based on prop details
            #     blue_motion_type = self.positioner.pictograph.blue_motion.motion_type
            #     red_motion_type = self.positioner.pictograph.red_motion.motion_type
            #     beta_ori = "radial" if object.motion.start_ori in [IN, OUT] else "nonradial"
            #     prop_loc = object.loc
            #     override_key = f"swap_beta_{prop_loc}_{beta_ori}_blue_{blue_motion_type}_red_{red_motion_type}"

            #     # Check if override key needs to be updated
            #     turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
            #     turn_data = existing_data[letter].get(turns_tuple, {})
            #     if override_key in turn_data:
            #         del turn_data[override_key]
            #     else:
            #         turn_data[override_key] = True

            #     existing_data[letter][turns_tuple] = turn_data

            # Write the updated data back to the file
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
        """Remove a specific motion entry from the special placements JSON file."""
        # Determine the orientation key and file path
        orientation_key = (
            "from_radial" if arrow.motion.start_ori in [IN, OUT] else "from_nonradial"
        )
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )

        # Load current data
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            letter_data = data.get(letter, {})

            # Remove the specific motion entry
            turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(
                letter
            )
            turn_data = letter_data.get(turns_tuple, {})

            motion_key = self.positioner.motion_key_generator.generate_motion_key(arrow)
            if motion_key in turn_data:
                del turn_data[motion_key]

                # Remove the turn entry if it's now empty
                if not turn_data:
                    del letter_data[turns_tuple]

            # Update the JSON file
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(
                    r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str
                )
                file.write(formatted_json_str)
        arrow.pictograph.main_widget.refresh_placements()
