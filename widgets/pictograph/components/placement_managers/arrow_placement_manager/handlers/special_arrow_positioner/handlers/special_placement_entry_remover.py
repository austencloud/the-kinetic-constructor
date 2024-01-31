import os
from typing import TYPE_CHECKING, Union
from Enums import LetterType
from constants import BLUE, CLOCK, COUNTER, IN, OUT, RED, Type1, Type4, Type5
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import Colors
from utilities.TypeChecking.letter_lists import Type1_hybrid_letters

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

    def remove_special_placement_entry(self, letter: str, arrow: Arrow) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)
        file_path = self._generate_file_path(ori_key, letter)

        if os.path.exists(file_path):
            data = self.data_updater.json_handler.load_json_data(file_path)
            if letter in data:
                letter_data = data[letter]
                turns_tuple = (
                    self.positioner.turns_tuple_generator.generate_turns_tuple(letter)
                )
                key = self._generate_key_for_removal(arrow)
                self._remove_turn_data_entry(letter_data, turns_tuple, key)

                if arrow.pictograph.check.starts_from_mixed_orientation():
                    other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
                    other_file_path = self._generate_file_path(other_ori_key, letter)
                    other_data = self.data_updater.json_handler.load_json_data(
                        other_file_path
                    )
                    other_letter_data = other_data.get(letter, {})
                    mirrored_tuple = self.data_updater.mirrored_entry_handler._generate_mirrored_tuple(
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
                    new_turns_tuple = self.data_updater.mirrored_entry_handler._generate_mirrored_tuple(
                        arrow
                    )
                    self._remove_turn_data_entry(
                        other_letter_data, new_turns_tuple, new_key
                    )

                # Write changes to the original file
                data[letter] = letter_data
                self.data_updater.json_handler.write_json_data(data, file_path)

            arrow.pictograph.main_widget.refresh_placements()

    def _generate_file_path(self, ori_key: str, letter: str) -> str:
        return os.path.join(
            self.positioner.placement_manager.pictograph.main_widget.parent_directory,
            f"{ori_key}/{letter}_placements.json",
        )

    def _generate_key_for_removal(self, arrow: Arrow) -> str:
        if arrow.pictograph.check.starts_from_mixed_orientation():
            layer = "layer1" if arrow.motion.start_ori in [IN, OUT] else "layer2"
            return f"{arrow.motion.motion_type}_from_{layer}"
        elif arrow.pictograph.letter in Type1_hybrid_letters:
            return arrow.motion.motion_type
        return arrow.color

    def _get_other_color(self, color: Colors) -> Colors:
        return RED if color == BLUE else BLUE

    def _remove_turn_data_entry(self, letter_data: dict, turns_tuple: str, key) -> None:
        turn_data = letter_data.get(turns_tuple, {})
        if key in turn_data:
            del turn_data[key]
            if not turn_data:
                del letter_data[turns_tuple]

    def _generate_key_for_removal(self, arrow: Arrow) -> str:
        if arrow.pictograph.check.starts_from_mixed_orientation():
            if arrow.pictograph.check.has_hybrid_motions():
                if arrow.motion.start_ori in [IN, OUT]:
                    layer = "layer1"
                elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                    layer = "layer2"
                return f"{arrow.motion.motion_type}_from_{layer}"
            elif not arrow.pictograph.check.has_hybrid_motions():
                return arrow.color
        elif arrow.pictograph.letter in Type1_hybrid_letters:
            return arrow.motion.motion_type
        return arrow.color
