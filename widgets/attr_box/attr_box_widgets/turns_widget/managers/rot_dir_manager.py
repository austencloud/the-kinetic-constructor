from typing import TYPE_CHECKING
from constants import *
from utilities.TypeChecking.TypeChecking import (
    PropRotDirs,
)
from utilities.TypeChecking.letter_lists import (
    Type2_letters,
    Type3_letters,
    Type4_letters,
)

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion
    from ..turns_widget import TurnsWidget


class RotationDirectionManager:
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
        """Determine the property rotation direction."""
        if (
            motion.pictograph.letter in Type2_letters
            or motion.pictograph.letter in Type3_letters
        ):
            if (
                not self.attr_box.vtg_dir_btn_state[SAME]
                and not self.attr_box.vtg_dir_btn_state[OPP]
            ):
                self._set_vtg_dir_state_default()
                self.turns_widget.attr_box.rot_dir_button_manager.show_vtg_dir_buttons()
            if self.attr_box.vtg_dir_btn_state[SAME]:
                return other_motion.prop_rot_dir
            if self.attr_box.vtg_dir_btn_state[OPP]:
                if other_motion.prop_rot_dir == CLOCKWISE:
                    return COUNTER_CLOCKWISE
                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    return CLOCKWISE

        elif motion.pictograph.letter in Type4_letters:
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
        self.attr_box.vtg_dir_btn_state[SAME] = True
        self.attr_box.vtg_dir_btn_state[OPP] = False
