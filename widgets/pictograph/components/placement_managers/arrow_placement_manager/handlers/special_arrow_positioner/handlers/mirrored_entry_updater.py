from Enums import LetterType
from constants import *
from objects.arrow.arrow import Arrow

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.handlers.special_arrow_positioner.handlers.special_placement_mirrored_entry_manager import (
        SpecialPlacementMirroredEntryManager,
    )
    from .special_placement_data_updater import SpecialPlacementDataUpdater
    from ....handlers.turns_tuple_generator.turns_tuple_generator import (
        TurnsTupleGenerator,
    )


class MirroredEntryUpdater:
    def __init__(
        self,
        special_placement_mirrored_entry_manager: "SpecialPlacementMirroredEntryManager",
    ):
        self.special_placement_mirrored_entry_manager = (
            special_placement_mirrored_entry_manager
        )
        self.data_updater = self.special_placement_mirrored_entry_manager.data_updater
        self.turns_tuple_generator = (
            self.special_placement_mirrored_entry_manager.turns_tuple_generator
        )

    def update_entry(self, letter: str, arrow: Arrow):
        letter_type = LetterType.get_letter_type(letter)
        ori_key = self.data_updater._get_ori_key(arrow.motion)
        other_motion = arrow.pictograph.get.other_motion(arrow.motion)
        letter_data, original_turn_data = (
            self._fetch_letter_data_and_original_turn_data(ori_key, letter, arrow)
        )

        if arrow.pictograph.check.starts_from_mixed_orientation():
            other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                letter, ori_key
            )
            mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                arrow
            )
            if not arrow.pictograph.check.starts_from_mixed_orientation():
                if (
                    letter_type in [Type1, Type5, Type6]
                    and arrow.motion.motion_type == other_motion.motion_type
                    and letter not in ["S", "T"]
                ):
                    attr = BLUE if arrow.color == RED else RED
                    if mirrored_turns_tuple not in other_letter_data:
                        other_letter_data[mirrored_turns_tuple] = {}
                    if attr not in other_letter_data[mirrored_turns_tuple]:
                        other_letter_data[mirrored_turns_tuple][attr] = {}
                    other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[
                        arrow.color
                    ]
                elif letter in ["S", "T"]:
                    attr = arrow.motion.lead_state
                    if mirrored_turns_tuple not in other_letter_data:
                        other_letter_data[mirrored_turns_tuple] = {}
                    if attr not in other_letter_data[mirrored_turns_tuple]:
                        other_letter_data[mirrored_turns_tuple][attr] = {}
                    other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[
                        arrow.motion.lead_state
                    ]
                else:
                    attr = arrow.motion.motion_type
                    if mirrored_turns_tuple not in other_letter_data:
                        other_letter_data[mirrored_turns_tuple] = {}
                    if attr not in other_letter_data[mirrored_turns_tuple]:
                        other_letter_data[mirrored_turns_tuple][attr] = {}
                    other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[
                        arrow.motion.motion_type
                    ]

                self.initialize_dicts(mirrored_turns_tuple, other_letter_data, attr)

            elif arrow.pictograph.check.starts_from_mixed_orientation():
                layer = 1 if arrow.motion.start_ori in [IN, OUT] else 2

                if (
                    letter_type in [Type1, Type5, Type6]
                    and arrow.motion.motion_type == other_motion.motion_type
                    and letter not in ["S", "T"]
                ):
                    key = BLUE if arrow.color == RED else RED
                    if mirrored_turns_tuple not in other_letter_data:
                        other_letter_data[mirrored_turns_tuple] = {}
                    self.initialize_dicts(mirrored_turns_tuple, other_letter_data, key)
                    other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[
                        arrow.color
                    ]

                elif letter in ["S", "T"]:
                    attr = arrow.motion.lead_state
                    key = f"{attr}_from_layer{layer}"

                    self.initialize_dicts(mirrored_turns_tuple, other_letter_data, key)
                    other_letter_data[mirrored_turns_tuple][key] = original_turn_data[
                        key
                    ]
                else:
                    attr = arrow.motion.motion_type
                    key = f"{attr}_from_layer{layer}"
                    self.initialize_dicts(mirrored_turns_tuple, other_letter_data, key)
                    other_letter_data[mirrored_turns_tuple][key] = original_turn_data[
                        key
                    ]

            self.data_updater.update_specific_entry_in_json(
                letter, other_letter_data, other_ori_key
            )

        # Save the updated data
        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)

    def initialize_dicts(self, mirrored_turns_tuple, other_letter_data, attr):
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        if attr not in other_letter_data[mirrored_turns_tuple]:
            other_letter_data[mirrored_turns_tuple][attr] = {}

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key, letter, arrow
    ) -> tuple[dict, dict]:
        letter_data = self._get_letter_data(ori_key, letter)
        original_turns_tuple = self._generate_turns_tuple(arrow)
        return letter_data, letter_data.get(original_turns_tuple, {})

    def _generate_turns_tuple(self, arrow: "Arrow") -> str:
        return self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)

    def _get_letter_data(self, ori_key: str, letter: str) -> dict:
        return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key, {}
        ).get(
            letter, {}
        )

    def _get_keys_for_mixed_start_ori(self, letter, ori_key) -> tuple[str, dict]:
        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_letter_data = self._get_letter_data(other_ori_key, letter)
        return other_ori_key, other_letter_data
