from Enums.Enums import LetterType

from Enums.letters import LetterConditions, Letter
from data.constants import *
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mirrored_entry_updater import MirroredEntryUpdater


class MirroredEntryUpdaterBase:
    def __init__(self, mirrored_entry_updater: "MirroredEntryUpdater", arrow: Arrow):
        self.mirrored_entry_updater = mirrored_entry_updater
        self.arrow = arrow

    def update_entry(self, letter: Letter, original_turn_data: dict):
        # Common update logic
        pass


class StandardOrientationUpdater(MirroredEntryUpdaterBase):
    def update_entry(self, letter: Letter, original_turn_data: dict):
        letter_type = LetterType.get_letter_type(letter)
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(
                self.arrow
            )
        )
        self._mirror_entry(mirrored_turns_tuple, letter)

    def _mirror_entry(self, mirrored_turns_tuple, letter: Letter):
        if letter.value in ["S", "T", "β"] or letter in Letter.get_letters_by_condition(
            LetterConditions.HYBRID
        ):
            return
        ori_key = self.mirrored_entry_updater.manager.data_updater._generate_ori_key(
            self.arrow.motion
        )

        letter_data = self.mirrored_entry_updater.manager.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key,
            {},
        ).get(
            letter.value, {}
        )
        turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_turns_tuple(
                self.arrow.pictograph
            )
        )

        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, letter_data, ori_key
        )
        if (
            not self.arrow.motion.turns
            == self.arrow.pictograph.get.other_arrow(self.arrow).turns
            and self.arrow.motion.motion_type
            == self.arrow.pictograph.get.other_arrow(self.arrow).motion.motion_type
        ):
            if mirrored_turns_tuple not in letter_data:
                letter_data[mirrored_turns_tuple] = {}
            letter_data[mirrored_turns_tuple][
                BLUE if self.arrow.color == RED else RED
            ] = letter_data[turns_tuple][self.arrow.color]
            self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
                letter, letter_data, ori_key
            )
        elif (
            not self.arrow.motion.turns
            == self.arrow.pictograph.get.other_arrow(self.arrow).turns
            and self.arrow.motion.motion_type
            != self.arrow.pictograph.get.other_arrow(self.arrow).motion.motion_type
        ):
            if mirrored_turns_tuple not in letter_data:
                letter_data[mirrored_turns_tuple] = {}
            letter_data[mirrored_turns_tuple][
                self.arrow.motion.motion_type
            ] = letter_data[turns_tuple][self.arrow.motion.motion_type]
            self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
                letter, letter_data, ori_key
            )

    def _determine_motion_attribute(self) -> str:
        letter = self.arrow.pictograph.letter
        if letter in ["S", "T"]:
            return self.arrow.motion.lead_state
        elif self.arrow.pictograph.check.has_hybrid_motions():
            return self.arrow.motion.motion_type
        else:
            return self.arrow.color


class MixedOrientationUpdater(MirroredEntryUpdaterBase):
    def update_entry(self, letter: Letter, original_turn_data: dict):
        mirrored_turns_tuple = (
            self.mirrored_entry_updater.turns_tuple_generator.generate_mirrored_tuple(
                self.arrow
            )
        )
        other_ori_key, other_letter_data = (
            self.mirrored_entry_updater._get_keys_for_mixed_start_ori(
                letter,
                self.mirrored_entry_updater.manager.data_updater._generate_ori_key(
                    self.arrow.motion
                ),
            )
        )
        layer = "1" if self.arrow.motion.start_ori in [IN, OUT] else "2"

        if letter in ["S", "T"]:
            attr = self.arrow.motion.lead_state
            key = f"{attr}_from_layer{layer}"
        elif self.arrow.pictograph.check.has_hybrid_motions():
            attr = self.arrow.motion.motion_type
            key = f"{attr}_from_layer{layer}"
        else:
            key = f"{BLUE if self.arrow.color == RED else RED}"

        self.mirrored_entry_updater._update_mirrored_entry_data(
            mirrored_turns_tuple, other_letter_data, key, original_turn_data, self.arrow
        )
        self.mirrored_entry_updater.manager.data_updater.update_specific_entry_in_json(
            letter, other_letter_data, other_ori_key
        )
