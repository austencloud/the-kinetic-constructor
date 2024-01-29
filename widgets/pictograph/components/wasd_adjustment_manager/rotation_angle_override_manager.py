from typing import TYPE_CHECKING, Optional
from Enums import LetterType
from constants import (
    BLUE,
    IN,
    OUT,
    RED,
    STATIC,
    DASH,
    Type2,
    Type3,
    Type4,
    Type5,
    Type6,
)
from PyQt6.QtCore import Qt
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion

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
        self.turns_tuple_generator = self.special_positioner.turns_tuple_generator

    def handle_rotation_angle_override(self, key: Qt.Key) -> None:
        if not self._is_valid_for_override():
            return

        ori_key = self._get_orientation_key()
        data = self.pictograph.main_widget.load_special_placements()
        letter = self.pictograph.letter

        self._apply_override_if_needed(letter, data, ori_key)
        for pictograph in self.pictograph.scroll_area.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def _is_valid_for_override(self) -> bool:
        return (
            self.pictograph.selected_arrow
            and self.pictograph.selected_arrow.motion.motion_type in [STATIC, DASH]
        )

    def _get_orientation_key(self) -> str:
        start_ori = self.pictograph.selected_arrow.motion.start_ori
        return "from_radial" if start_ori in [IN, OUT] else "from_nonradial"

    def _apply_override_if_needed(self, letter: str, data: dict, ori_key: str) -> None:
        letter_type = LetterType.get_letter_type(letter)
        rot_angle_key = self._determine_rot_angle_key(letter_type)
        turns_tuple = self.turns_tuple_generator.generate_turns_tuple(letter)
        self._apply_rotation_override(letter, data, ori_key, turns_tuple, rot_angle_key)

    def _determine_rot_angle_key(self, letter_type: LetterType) -> str:
        if letter_type in [Type5, Type6]:
            return f"{self.pictograph.selected_arrow.color}_rot_angle"

        else:
            return f"{self.pictograph.selected_arrow.motion.motion_type}_rot_angle"

    def _apply_rotation_override(
        self,
        letter: str,
        data: dict,
        ori_key: str,
        adjustment_key_str: str,
        rot_angle_key: str,
    ) -> None:
        letter_data = data[ori_key].get(letter, {})
        turn_data = letter_data.get(adjustment_key_str, {})

        if rot_angle_key in turn_data:
            del turn_data[rot_angle_key]
        else:
            turn_data[rot_angle_key] = 0

        letter_data[adjustment_key_str] = turn_data
        data[ori_key][letter] = letter_data

        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter, letter_data, self.pictograph.selected_arrow
        )

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = (
            self.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        ori_key = (
            "from_radial" if arrow.motion.start_ori in [IN, OUT] else "from_nonradial"
        )
        letter = arrow.scene.letter
        letter_data = placements[ori_key].get(letter, {})
        turns_tuple = (
            self.special_positioner.turns_tuple_generator.generate_turns_tuple(letter)
        )
        letter_type = LetterType.get_letter_type(letter)
        return letter_data.get(turns_tuple, {}).get(
            f"{arrow.color}_rot_angle"
            if letter_type in [Type5, Type6]
            else f"{arrow.motion.motion_type}_rot_angle"
        )
