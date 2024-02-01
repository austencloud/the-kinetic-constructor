from typing import TYPE_CHECKING, Optional
from Enums import LetterType
from constants import (
    BLUE,
    DASH,
    IN,
    OUT,
    RED,
    STATIC,
    Type5,
    Type6,
)
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .special_placement_data_updater import SpecialPlacementDataUpdater


class SpecialPlacementMirroredEntryManager:
    def __init__(self, data_updater: "SpecialPlacementDataUpdater") -> None:
        self.data_updater = data_updater
        self.turns_tuple_generator = (
            data_updater.positioner.placement_manager.pictograph.main_widget.turns_tuple_generator
        )

    def update_mirrored_entry_in_json(self, arrow: "Arrow") -> None:
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)
        mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(arrow)
        if mirrored_turns_tuple:
            self._create_or_update_mirrored_entry(arrow.pictograph.letter, arrow)
        self._update_pictographs_in_section(letter_type)

    def _create_or_update_mirrored_entry(self, letter: str, arrow: Arrow) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)
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
            if (
                arrow.pictograph.letter in ["S", "T"]
                or arrow.pictograph.check.has_hybrid_motions()
            ):
                attr = self.data_updater.positioner.motion_key_generator.get_key(arrow)
                if mirrored_turns_tuple not in other_letter_data:
                    other_letter_data[mirrored_turns_tuple] = {}
                if attr not in original_turn_data:
                    original_turn_data[attr] = {}
                other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[attr]

            elif not arrow.pictograph.check.has_hybrid_motions():

                attr = "blue" if arrow.color == "red" else "red"
                if mirrored_turns_tuple not in other_letter_data:
                    other_letter_data[mirrored_turns_tuple] = {}
                if attr not in other_letter_data[mirrored_turns_tuple]:
                    other_letter_data[mirrored_turns_tuple][attr] = {}
                if arrow.color not in original_turn_data:
                    original_turn_data[arrow.color] = {}
                other_letter_data[mirrored_turns_tuple][attr] = original_turn_data[
                    arrow.color
                ]

            self.initialize_dicts(mirrored_turns_tuple, other_letter_data, attr)
            self.data_updater.update_specific_entry_in_json(
                letter, other_letter_data, other_ori_key
            )
            mirrored_turn_data = self._prepare_mirrored_turn_data(
                arrow, original_turn_data
            )
            if self._should_handle_rotation_angle(arrow):
                rotation_angle_override = self._check_for_rotation_angle_override(
                    original_turn_data
                )
                if rotation_angle_override is not None:
                    self._apply_rotation_angle_override(
                        mirrored_turn_data, rotation_angle_override, arrow
                    )
                    self._handle_mirrored_rotation_angle_override(
                        other_letter_data,
                        arrow,
                        rotation_angle_override,
                        mirrored_turns_tuple,
                    )

        self.data_updater.update_specific_entry_in_json(letter, letter_data, ori_key)

    def update_rotation_angle_in_mirrored_entry(
        self, letter: str, arrow: Arrow, rot_angle_key: str
    ) -> None:
        self.rot_angle_override_manager = (
            self.data_updater.positioner.placement_manager.pictograph.wasd_manager.rotation_angle_override_manager
        )

        ori_key = self.data_updater._get_ori_key(arrow.motion)
        _, original_turn_data = self._fetch_letter_data_and_original_turn_data(
            ori_key, letter, arrow
        )

        if self._should_handle_rotation_angle(arrow):
            rotation_angle_override = self._check_for_rotation_angle_override(
                original_turn_data
            )
            if rotation_angle_override is not None:
                other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                    letter, ori_key
                )
                mirrored_turns_tuple = (
                    self.turns_tuple_generator.generate_mirrored_tuple(arrow)
                )
                self.rot_angle_override_manager._handle_mirrored_rotation_angle_override(
                    other_letter_data,
                    arrow,
                    rotation_angle_override,
                    mirrored_turns_tuple,
                )
                self.data_updater.update_specific_entry_in_json(
                    letter, other_letter_data, other_ori_key
                )

    def remove_rotation_angle_in_mirrored_entry(
        self, letter: str, arrow: Arrow, hybrid_key: str
    ) -> None:
        ori_key = self.data_updater._get_ori_key(arrow.motion)

        if arrow.pictograph.check.starts_from_mixed_orientation():
            other_ori_key, other_letter_data = self._get_keys_for_mixed_start_ori(
                letter, ori_key
            )
            mirrored_turns_tuple = self.turns_tuple_generator.generate_mirrored_tuple(
                arrow
            )

            if hybrid_key in other_letter_data.get(mirrored_turns_tuple, {}):
                del other_letter_data[mirrored_turns_tuple][hybrid_key]

            self.data_updater.update_specific_entry_in_json(
                letter, other_letter_data, other_ori_key
            )

    def initialize_dicts(self, mirrored_turns_tuple, other_letter_data, attr):
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        if attr not in other_letter_data[mirrored_turns_tuple]:
            other_letter_data[mirrored_turns_tuple][attr] = {}

    def _get_keys_for_mixed_start_ori(self, letter, ori_key) -> tuple[str, dict]:
        other_ori_key = self.data_updater.get_other_layer3_ori_key(ori_key)
        other_letter_data = self._get_letter_data(other_ori_key, letter)
        return other_ori_key, other_letter_data

    def _fetch_letter_data_and_original_turn_data(
        self, ori_key, letter, arrow
    ) -> tuple[dict, dict]:
        letter_data = self._get_letter_data(ori_key, letter)
        original_turns_tuple = self._generate_turns_tuple(arrow)
        return letter_data, letter_data.get(original_turns_tuple, {})

    def _prepare_mirrored_turn_data(
        self, arrow: Arrow, original_turn_data: dict[str, bool]
    ) -> dict:
        mirrored_turn_data = {}
        letter_type = LetterType.get_letter_type(arrow.pictograph.letter)
        default_adjustment = self.data_updater.positioner.placement_manager.default_positioner.get_default_adjustment(
            arrow
        )

        if letter_type in [Type5, Type6]:
            other_arrow = arrow.pictograph.get.other_arrow(arrow)
            if arrow.turns > 0 and other_arrow.turns > 0:
                other_color = "blue" if arrow.color == "red" else "red"
                for key in list(original_turn_data.keys()):
                    if arrow.color in key:
                        new_key = key.replace(arrow.color, other_color)
                        mirrored_turn_data[new_key] = default_adjustment
                mirrored_turn_data[other_color] = original_turn_data.get(
                    arrow.color, default_adjustment
                )
            elif arrow.turns > 0 or other_arrow.turns > 0:
                mirrored_turn_data[arrow.color] = original_turn_data.get(
                    arrow.color, default_adjustment
                )
        else:
            if arrow.pictograph.check.starts_from_mixed_orientation():
                if arrow.pictograph.check.has_hybrid_motions():
                    for key in original_turn_data:
                        mirrored_turn_data[key] = default_adjustment
                else:
                    color_key = RED if arrow.color == BLUE else BLUE
                    mirrored_turn_data[color_key] = original_turn_data.get(
                        arrow.color, default_adjustment
                    )

        return mirrored_turn_data

    def _should_handle_rotation_angle(self, arrow: Arrow) -> bool:
        return arrow.motion.motion_type in [STATIC, DASH]

    def _apply_rotation_angle_override(
        self, mirrored_turn_data, rotation_angle_override, arrow
    ):
        other_color = "blue" if arrow.color == "red" else "red"
        mirrored_turn_data[f"{other_color}_rot_angle"] = rotation_angle_override

    def _check_for_rotation_angle_override(self, turn_data: dict) -> Optional[int]:
        for key in turn_data:
            if "rot_angle" in key:
                return turn_data[key]
        return None

    def _update_pictographs_in_section(self, letter_type: LetterType) -> None:
        section = self.data_updater.positioner.pictograph.scroll_area.sections_manager.get_section(
            letter_type
        )
        for pictograph in section.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def _get_letter_data(self, ori_key: str, letter: str) -> dict:
        return self.data_updater.positioner.placement_manager.pictograph.main_widget.special_placements.get(
            ori_key, {}
        ).get(
            letter, {}
        )

    def _generate_turns_tuple(self, arrow: "Arrow") -> str:
        return self.turns_tuple_generator.generate_turns_tuple(arrow.pictograph)
