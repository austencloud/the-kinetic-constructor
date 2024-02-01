import os
from typing import TYPE_CHECKING
from constants import BLUE, special_placements_parent_directory, RED
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementEntryRemover:
    """Handles removal of special placement entries."""

    def __init__(
        self,
        data_updater: "SpecialPlacementDataUpdater",
    ) -> None:
        self.positioner = data_updater.positioner
        self.data_updater = data_updater
        self.turns_tuple_generator = self.positioner.placement_manager.pictograph.main_widget.turns_tuple_generator

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)
        file_path = self._generate_file_path(ori_key, letter)

        if os.path.exists(file_path):
            data = self.data_updater.json_handler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = self.turns_tuple_generator.generate_turns_tuple(
                    self.positioner.placement_manager.pictograph
                )
                key = self.data_updater.positioner.motion_key_generator.get_key(arrow)
                self._remove_turn_data_entry(letter_data, turns_tuple, key)

                if arrow.pictograph.check.starts_from_mixed_orientation():
                    other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
                    other_file_path = self._generate_file_path(other_ori_key, letter)
                    other_data = self.data_updater.json_handler.load_json_data(
                        other_file_path
                    )
                    other_letter_data = other_data.get(letter, {})
                    mirrored_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                        arrow
                    )
                    if key == BLUE:
                        new_key = RED
                    elif key == RED:
                        new_key = BLUE
                    else:
                        new_key = key
                    if other_letter_data != letter_data:
                        if mirrored_tuple not in other_letter_data:
                            other_letter_data[mirrored_tuple] = {}
                        if new_key not in other_letter_data[mirrored_tuple]:
                            if turns_tuple in letter_data:
                                if key not in letter_data[turns_tuple]:
                                    letter_data[turns_tuple][key] = {}
                                other_letter_data[mirrored_tuple][new_key] = (
                                    letter_data[turns_tuple][key]
                                )
                        if turns_tuple not in letter_data:
                            del other_data[letter][mirrored_tuple]

                        elif key not in letter_data[turns_tuple]:
                            del other_data[letter][mirrored_tuple][new_key]
                        self.data_updater.json_handler.write_json_data(
                            other_data, other_file_path
                        )
                    new_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                        arrow
                    )
                    self._remove_turn_data_entry(
                        other_letter_data, new_turns_tuple, new_key
                    )

                data[letter] = letter_data
                self.data_updater.json_handler.write_json_data(data, file_path)

            arrow.pictograph.main_widget.refresh_placements()

    def _generate_file_path(self, ori_key: str, letter: str) -> str:
        return os.path.join(
            special_placements_parent_directory,
            f"{ori_key}/{letter}_placements.json",
        )

    def _get_other_color(self, color: Colors) -> Colors:
        return RED if color == BLUE else BLUE

    def _remove_turn_data_entry(self, letter_data: dict, turns_tuple: str, key) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if key in turn_data:
            del turn_data[key]
            if not turn_data:
                del letter_data[turns_tuple]
