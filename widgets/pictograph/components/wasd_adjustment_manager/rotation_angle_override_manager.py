from typing import TYPE_CHECKING, Optional
from constants import IN, OUT, STATIC, DASH
from PyQt6.QtCore import Qt
from objects.arrow.arrow import Arrow
from widgets.pictograph.components.wasd_adjustment_manager.rotation_angle_override_key_generator import (
    RotationAngleOverrideKeyGenerator,
)
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from ..wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager


class RotationAngleOverrideManager:
    """
    Manages rotation angle overrides for arrows in a pictograph based on specific letter types and motions.

    This class handles special cases where the rotation angle of an arrow needs to be overridden, based on the data
    defined in the "{letter}_placements.json" file.
    """

    def __init__(self, wasd_adjustment_manager: "WASD_AdjustmentManager") -> None:
        self.wasd_manager = wasd_adjustment_manager
        self.pictograph = wasd_adjustment_manager.pictograph
        self.special_positioner = (
            self.pictograph.arrow_placement_manager.special_positioner
        )
        self.turns_tuple_generator = self.pictograph.main_widget.turns_tuple_generator
        self.key_generator = RotationAngleOverrideKeyGenerator(self)

    def handle_rotation_angle_override(self, key: Qt.Key) -> None:
        if not self._is_valid_for_override():
            return

        ori_key = self.special_positioner.data_updater.get_ori_key(
            self.pictograph.selected_arrow.motion
        )
        data = self.pictograph.main_widget.special_placements
        letter = self.pictograph.letter

        self._apply_override_if_needed(letter, data, ori_key)
        self.pictograph.arrow_placement_manager.update_arrow_placements()
        QApplication.processEvents()
        visible_pictographs = self.get_visible_pictographs()
        for pictograph in visible_pictographs:
            pictograph.arrow_placement_manager.update_arrow_placements()

    def get_visible_pictographs(self) -> list["Pictograph"]:
        visible_pictographs = []
        for pictograph_list in self.pictograph.main_widget.all_pictographs.values():
            for pictograph in pictograph_list.values():
                if pictograph.view.isVisible():
                    visible_pictographs.append(pictograph)
        return visible_pictographs

    def _is_valid_for_override(self) -> bool:
        return (
            self.pictograph.selected_arrow
            and self.pictograph.selected_arrow.motion.motion_type in [STATIC, DASH]
        )

    def _apply_override_if_needed(self, letter: str, data: dict, ori_key: str) -> None:
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key(
            self.pictograph.selected_arrow
        )
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(self.pictograph)
        self._apply_rotation_override(letter, data, ori_key, turns_tuple, rot_angle_key)

    def _apply_rotation_override(
        self,
        letter: str,
        data: dict,
        ori_key: str,
        turns_tuple: str,
        rot_angle_key: str,
    ) -> None:
        letter_data = data[ori_key].get(letter, {})
        turn_data = letter_data.get(turns_tuple, {})

        letter_data[turns_tuple] = turn_data
        data[ori_key][letter] = letter_data
        if rot_angle_key in turn_data:
            del turn_data[rot_angle_key]
            self._update_mirrored_entry_with_rotation_override_removal(rot_angle_key)
        else:
            turn_data[rot_angle_key] = True
            self._update_mirrored_entry_with_rotation_override(turn_data)
        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter, letter_data, ori_key
        )
        self.pictograph.updater.update_pictograph()

    def handle_mirrored_rotation_angle_override(
        self, other_letter_data, rotation_angle_override, mirrored_turns_tuple
    ):
        rot_angle_key = self.key_generator.generate_rotation_angle_override_key()
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][rot_angle_key] = rotation_angle_override

    def _update_mirrored_entry_with_rotation_override(self, updated_turn_data: dict):
        mirrored_entry_manager = (
            self.wasd_manager.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        mirrored_entry_manager.rot_angle_manager.update_rotation_angle_in_mirrored_entry(
            self.pictograph.selected_arrow, updated_turn_data
        )

    def _update_mirrored_entry_with_rotation_override_removal(self, hybrid_key: str):
        mirrored_entry_handler = (
            self.wasd_manager.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        if mirrored_entry_handler:
            mirrored_entry_handler.rot_angle_manager.remove_rotation_angle_in_mirrored_entry(
                self.pictograph.selected_arrow, hybrid_key
            )

    def _generate_rotation_angle_key(self, arrow: Arrow) -> str:
        motion_type = arrow.motion.motion_type
        if arrow.pictograph.check.starts_from_mixed_orientation():
            layer = "layer1" if arrow.motion.start_ori in [IN, OUT] else "layer2"
            return f"{motion_type}_from_{layer}_rot_angle_override"
        return f"{motion_type}_rot_angle_override"

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = (
            self.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        ori_key = self.special_positioner.data_updater.get_ori_key(arrow.motion)
        letter = arrow.pictograph.letter
        letter_data = placements[ori_key].get(letter, {})
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(self.pictograph)

        key = self._generate_rotation_angle_key(arrow)

        if turns_tuple not in letter_data:
            letter_data[turns_tuple] = {}
        return letter_data[turns_tuple].get(key)
