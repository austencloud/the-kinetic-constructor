from typing import TYPE_CHECKING
from constants import *
from utilities.TypeChecking.MotionAttributes import PropRotDirs
from utilities.TypeChecking.letter_lists import (
    Type2_letters,
    Type3_letters,
    Type4_letters,
)

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..turns_widget import TurnsWidget


class RotDirManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.attr_box = turns_widget.attr_box
        self.turns_widget = turns_widget

    def _set_prop_rot_dir_based_on_vtg_state(self, motion: "Motion") -> None:
        """Set the rotation direction of the motion based on the vtg directional relationship."""
        other_motion = motion.pictograph.get.other_motion(motion)
        motion.prop_rot_dir = self._determine_prop_rot_dir(motion, other_motion)

    def _determine_prop_rot_dir(
        self, motion: "Motion", other_motion: "Motion"
    ) -> PropRotDirs:
        """Determine the prop rot dir of the motion based on the vtg directional relationship."""
        letter = motion.pictograph.letter
        vtg_dir_state = self.attr_box.vtg_dir_btn_state

        same_dir_selected = (True, False)
        opp_dir_selected = (False, True)
        neither_dir_selected = (False, False)

        rotation_mapping = {
            same_dir_selected: other_motion.prop_rot_dir,
            opp_dir_selected: COUNTER_CLOCKWISE
            if other_motion.prop_rot_dir == CLOCKWISE
            else CLOCKWISE,
            neither_dir_selected: CLOCKWISE
            if other_motion.prop_rot_dir == NO_ROT
            else COUNTER_CLOCKWISE,
        }

        if letter in Type2_letters or letter in Type3_letters:
            if not any(vtg_dir_state.values()):
                self._set_vtg_dir_state_default()
                self.turns_widget.attr_box.rot_dir_button_manager.show_vtg_dir_buttons()

            return rotation_mapping[(vtg_dir_state[SAME], vtg_dir_state[OPP])]

        elif letter in Type4_letters:
            if other_motion.prop_rot_dir == NO_ROT:
                self.turns_widget.attr_box.rot_dir_button_manager.show_prop_rot_dir_buttons()
                self.turns_widget.attr_box.rot_dir_button_manager.cw_button.press()
                return CLOCKWISE
            elif other_motion.prop_rot_dir in [CLOCKWISE, COUNTER_CLOCKWISE]:
                self.turns_widget.attr_box.rot_dir_button_manager.show_vtg_dir_buttons()
                self.turns_widget.attr_box.rot_dir_button_manager.cw_button.press()
                return COUNTER_CLOCKWISE

    def _set_vtg_dir_state_default(self) -> None:
        """Set the vtg direction state to default."""
        self.attr_box.vtg_dir_btn_state = {SAME: True, OPP: False}
