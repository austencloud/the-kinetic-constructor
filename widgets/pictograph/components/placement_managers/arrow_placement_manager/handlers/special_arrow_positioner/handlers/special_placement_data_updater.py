import json
import os
import re
from typing import TYPE_CHECKING, Union
import logging

from Enums import LetterType
from constants import IN, OUT, Type1
from objects.arrow.arrow import Arrow
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Letters
from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class SpecialPlacementDataUpdater:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def update_arrow_adjustments_in_json(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        """Update the arrow's position adjustments in the JSON file."""
        if not arrow:
            return

        letter = self.positioner.pictograph.letter
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        orientation_key = self._get_orientation_key(arrow.motion.start_ori)

        letter_data = self._get_letter_data(letter, orientation_key)
        # Update turn data and save letter data
        self._update_or_create_turn_data(letter_data, turns_tuple, arrow, adjustment)
        self._save_letter_data(letter, letter_data, orientation_key)

        # Updated logging to include current values in the list
        logging.info(
            f"Updated {letter} in {orientation_key} at {turns_tuple} with adjustment {adjustment}. "
            f"Current values: {letter_data.get(turns_tuple)}"
        )

    def _get_letter_data(self, letter: str, orientation_key: str) -> dict:
        """Retrieve the letter data for a specific orientation from the special placements."""
        return (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                orientation_key
            ].get(letter, {})
        )

    def _update_or_create_turn_data(
        self,
        letter_data: dict,
        turns_tuple: str,
        arrow: "Arrow",
        adjustment: tuple[int, int],
    ) -> None:
        """Update existing turn data or create new turn data for the given adjustment."""
        turn_data = letter_data.get(turns_tuple, {})
        key = self.positioner.motion_key_generator.generate_motion_key(arrow)

        if key in turn_data:
            turn_data[key][0] += adjustment[0]
            turn_data[key][1] += adjustment[1]
        else:
            default_adjustment = self._get_default_adjustment(arrow)
            turn_data[key] = [
                default_adjustment[0] + adjustment[0],
                default_adjustment[1] + adjustment[1],
            ]

        letter_data[turns_tuple] = turn_data

    def _get_default_adjustment(self, arrow: "Arrow") -> tuple[int, int]:
        """Get default adjustment values for an arrow."""
        default_mgr = (
            self.positioner.pictograph.arrow_placement_manager.default_positioner
        )
        return default_mgr.get_default_adjustment(arrow)

    def _save_letter_data(
        self, letter: str, letter_data: dict, orientation_key: str
    ) -> None:
        """Save the updated letter data back to the JSON file in preferred format."""
        try:
            base_directory = (
                self.positioner.placement_manager.pictograph.main_widget.parent_directory
            )
            file_path = os.path.join(
                base_directory, orientation_key, f"{letter}_placements.json"
            )
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            existing_data = self._load_json_data(file_path)
            existing_data[letter] = letter_data
            self._write_json_data(existing_data, file_path)
        except Exception as e:
            logging.error(f"Error in saving letter data: {e}")

    def update_specific_entry_in_json(
        self, letter: Letters, letter_data: dict, object: Union[Arrow, Prop]
    ) -> None:
        try:
            orientation_key = self._get_orientation_key(object.motion.start_ori)
            base_directory = (
                self.positioner.placement_manager.pictograph.main_widget.parent_directory
            )
            file_path = os.path.join(
                base_directory, orientation_key, f"{letter}_placements.json"
            )

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            existing_data = self._load_json_data(file_path)
            existing_data[letter] = letter_data

            self._write_json_data(existing_data, file_path)

        except Exception as e:
            logging.error(f"Error in update_specific_entry_in_json: {e}")

    def _process_turn_data(
        self, turn_data: dict, arrow: "Arrow", adjustment: tuple[int, int]
    ) -> None:
        key = self.positioner.motion_key_generator.generate_motion_key(arrow)
        if key in turn_data:
            turn_data[key][0] += adjustment[0]
            turn_data[key][1] += adjustment[1]
        else:
            default_adjustment = self._get_default_data(arrow)
            turn_data[key] = [
                default_adjustment[0] + adjustment[0],
                default_adjustment[1] + adjustment[1],
            ]

    def _get_default_data(self, arrow: "Arrow") -> tuple[int, int]:
        default_mgr = (
            self.positioner.pictograph.arrow_placement_manager.default_positioner
        )
        default_turn_data = default_mgr.get_default_adjustment(arrow)
        return (default_turn_data[0], default_turn_data[1])

    def _create_default_turn_data(
        self, arrow: "Arrow", adjustment: tuple[int, int]
    ) -> dict:
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
        if (
            not LetterType.get_letter_type(arrow.pictograph.letter) == Type1
            or arrow.pictograph.letter not in Type1_non_hybrid_letters
        ):
            return

        orientation_key = self._get_orientation_key(arrow.motion.start_ori)
        file_path = os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{orientation_key}/{letter}_placements.json",
        )

        if os.path.exists(file_path):
            data = self._load_json_data(file_path)

            if letter in data:
                letter_data = data[letter]
                turns_tuple = (
                    self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                )
                mirrored_turns_tuple = self._mirror_turns_tuple(turns_tuple)

                self._remove_turn_data_entry(letter_data, turns_tuple, arrow.color)
                mirrored_color = "blue" if arrow.color == "red" else "red"
                self._remove_turn_data_entry(
                    letter_data, mirrored_turns_tuple, mirrored_color
                )

                self._write_json_data(data, file_path)

        arrow.pictograph.main_widget.refresh_placements()

    def _remove_turn_data_entry(self, letter_data, turns_tuple, color):
        turn_data = letter_data.get(turns_tuple, {})
        if color in turn_data:
            del turn_data[color]
            if not turn_data:
                del letter_data[turns_tuple]

    def update_mirrored_entry_in_json(
        self, adjustment: tuple[int, int], arrow: "Arrow"
    ) -> None:
        if (
            not LetterType.get_letter_type(arrow.pictograph.letter) == Type1
            or arrow.pictograph.letter not in Type1_non_hybrid_letters
        ):
            return

        letter = self.positioner.pictograph.letter
        turns_tuple = self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
        mirrored_turns_tuple = self._mirror_turns_tuple(turns_tuple)
        if not mirrored_turns_tuple:
            return
        orientation_key = self._get_orientation_key(arrow.motion.start_ori)
        letter_data = (
            self.positioner.placement_manager.pictograph.main_widget.special_placements[
                orientation_key
            ].get(letter, {})
        )

        original_turn_data = letter_data.get(turns_tuple, {})
        existing_adjustment = original_turn_data.get(arrow.color, adjustment)

        mirrored_color = "blue" if arrow.color == "red" else "red"
        mirrored_turn_data = letter_data.get(mirrored_turns_tuple, {})
        mirrored_turn_data[mirrored_color] = existing_adjustment

        letter_data[mirrored_turns_tuple] = mirrored_turn_data
        self.positioner.placement_manager.pictograph.main_widget.special_placements[
            letter
        ] = letter_data
        self.update_specific_entry_in_json(letter, letter_data, arrow)

    def _mirror_turns_tuple(self, turns_tuple: str) -> str:
        x, y = turns_tuple.strip("()").split(", ")
        return f"({y}, {x})" if x != y else None

    def _load_json_data(self, file_path) -> dict:
        try:
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as file:
                    return json.load(file)
            return {}
        except Exception as e:
            logging.error(f"Error loading JSON data from {file_path}: {e}")
            return {}

    def _write_json_data(self, data, file_path) -> None:
        """Write JSON data to a file with specific formatting."""
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                formatted_json_str = json.dumps(data, indent=2, ensure_ascii=False)
                formatted_json_str = re.sub(r"\[\s+(-?\d+),\s+(-?\d+)\s+\]", r"[\1, \2]", formatted_json_str)
                file.write(formatted_json_str)
            # logging.info(f"Data successfully written to {file_path}")
        except IOError as e:
            logging.error(f"Failed to write to {file_path}: {e}")

    def _get_orientation_key(self, motion_start_ori) -> str:
        return "from_radial" if motion_start_ori in [IN, OUT] else "from_nonradial"
