from typing import TYPE_CHECKING, Optional
from Enums import LetterType
from constants import CLOCK, COUNTER, IN, OUT, STATIC, DASH, Type5, Type6
from PyQt6.QtCore import Qt
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
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

    def handle_rotation_angle_override(self, key: Qt.Key) -> None:
        if not self._is_valid_for_override():
            return

        ori_key = self.special_positioner.data_updater._get_ori_key(
            self.pictograph.selected_arrow.motion
        )
        data = (
            self.pictograph.main_widget.special_placement_loader.load_special_placements()
        )
        letter = self.pictograph.letter

        self._apply_override_if_needed(letter, data, ori_key)
        for pictograph in self.pictograph.scroll_area.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def _is_valid_for_override(self) -> bool:
        return (
            self.pictograph.selected_arrow
            and self.pictograph.selected_arrow.motion.motion_type in [STATIC, DASH]
        )

    def _apply_override_if_needed(self, letter: str, data: dict, ori_key: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        rot_angle_key = self._determine_rot_angle_key(letter_type)
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(self.pictograph)
        self._apply_rotation_override(letter, data, ori_key, turns_tuple, rot_angle_key)

    def _determine_rot_angle_key(self, letter_type: LetterType) -> str:
        if self.pictograph.check.starts_from_mixed_orientation():
            if self.pictograph.check.has_hybrid_motions():
                return f"{self.pictograph.selected_arrow.motion.motion_type}_rot_angle"

        elif letter_type in [Type5, Type6]:
            return f"{self.pictograph.selected_arrow.color}_rot_angle_override"
        else:
            return f"{self.pictograph.selected_arrow.motion.motion_type}_rot_angle_override"

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

        hybrid_key = self._generate_hybrid_key_if_needed(
            self.pictograph.selected_arrow, rot_angle_key
        )

        if hybrid_key in turn_data:
            del turn_data[hybrid_key]
            self._update_mirrored_entry_with_rotation_override_removal(
                letter, self.pictograph.selected_arrow, hybrid_key
            )
        else:
            turn_data[hybrid_key] = True
            self._update_mirrored_entry_with_rotation_override(
                letter, self.pictograph.selected_arrow
            )

        letter_data[turns_tuple] = turn_data
        data[ori_key][letter] = letter_data
        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter, letter_data, ori_key
        )

    def handle_mirrored_rotation_angle_override(
        self, other_letter_data, arrow, rotation_angle_override, mirrored_turns_tuple
    ):
        """
        Updates the rotation angle override in the mirrored entry.
        """
        rot_angle_key = self._generate_rotation_angle_key(arrow)
        if mirrored_turns_tuple not in other_letter_data:
            other_letter_data[mirrored_turns_tuple] = {}
        other_letter_data[mirrored_turns_tuple][rot_angle_key] = rotation_angle_override

    def _update_mirrored_entry_with_rotation_override(
        self, letter: str, arrow: Arrow
    ):
        """
        Updates the mirrored entry to reflect a new rotation angle override.
        """
        mirrored_entry_handler = (
            self.wasd_manager.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        if mirrored_entry_handler:
            mirrored_entry_handler.update_rotation_angle_in_mirrored_entry(
                letter, arrow
            )

    def _update_mirrored_entry_with_rotation_override_removal(
        self, letter: str, arrow: Arrow, hybrid_key: str
    ):
        """
        Updates the mirrored entry to reflect the removal of a rotation angle override.
        """
        mirrored_entry_handler = (
            self.wasd_manager.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_manager
        )
        if mirrored_entry_handler:
            mirrored_entry_handler.remove_rotation_angle_in_mirrored_entry(
                letter, arrow, hybrid_key
            )

    def _generate_rotation_angle_key(self, arrow: Arrow) -> str:
        """
        Generates a key for rotation angle override based on the arrow's properties.
        """
        motion_type = arrow.motion.motion_type
        if arrow.pictograph.check.starts_from_mixed_orientation():
            layer = "layer1" if arrow.motion.start_ori in [IN, OUT] else "layer2"
            return f"{motion_type}_rot_angle_from_{layer}"
        return f"{motion_type}_rot_angle"

    def _generate_hybrid_key_if_needed(self, arrow: Arrow, rot_angle_key: str) -> str:
        if arrow.pictograph.check.starts_from_mixed_orientation():
            if self.pictograph.selected_arrow.motion.start_ori in [IN, OUT]:
                layer = "layer1"
            elif self.pictograph.selected_arrow.motion.start_ori in [CLOCK, COUNTER]:
                layer = "layer2"
            return f"{rot_angle_key}_from_{layer}"
        return rot_angle_key

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = (
            self.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        ori_key = self.special_positioner.data_updater._get_ori_key(arrow.motion)
        letter = arrow.scene.letter
        letter_data = placements[ori_key].get(letter, {})
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(self.pictograph)
        letter_type = LetterType.get_letter_type(letter)

        if arrow.motion.start_ori in [IN, OUT]:
            layer = "layer1"
        elif arrow.motion.start_ori in [CLOCK, COUNTER]:
            layer = "layer2"

        if self.pictograph.check.starts_from_mixed_orientation():
            if self.pictograph.check.has_hybrid_motions():
                if turns_tuple not in letter_data:
                    return None
                return letter_data[turns_tuple].get(
                    f"{arrow.motion.motion_type}_rot_angle_from_{layer}"
                )
        else:
            return letter_data.get(turns_tuple, {}).get(
                f"{arrow.color}_rot_angle"
                if letter_type in [Type5, Type6]
                else f"{arrow.motion.motion_type}_rot_angle"
            )
