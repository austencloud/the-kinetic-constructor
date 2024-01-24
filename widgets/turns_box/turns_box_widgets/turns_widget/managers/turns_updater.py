from typing import TYPE_CHECKING, Union
from constants import *
from utilities.TypeChecking.TypeChecking import (
    PropRotDirs,
    Turns,
)
from utilities.TypeChecking.letter_lists import (
    Type2_letters,
    Type3_letters,
    Type4_letters,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion
    from widgets.turns_box.turns_box_widgets.turns_widget.turns_widget import (
        TurnsWidget,
    )


class TurnsUpdater:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_box = turns_widget.turns_box
        self.turns_widget = turns_widget
        self.rot_dir_button_manager = (
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager
        )
        
    def update_motion_properties(self, motion: "Motion", new_turns: Turns) -> None:
        self._update_turns_and_rotation(motion, new_turns)
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _adjust_turns_for_pictograph(
        self, pictograph: "Pictograph", adjustment: Turns
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.motions.values():
            if self.turns_widget.relevance_checker.is_motion_relevant(motion):
                new_turns = self._calculate_new_turns(motion.turns, adjustment)
                self.update_motion_properties(motion, new_turns)

    def _calculate_new_turns(self, current_turns: Turns, adjustment: Turns) -> Turns:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns.is_integer() else new_turns

    def _update_turns_and_rotation(self, motion: "Motion", new_turns: Turns) -> None:
        """Update motion's turns and rotation properties based on new turn value."""
        if motion.motion_type in [DASH, STATIC]:
            self._handle_static_dash_motion(motion, new_turns)
        motion.turns_manager.set_motion_turns(new_turns)

    def _handle_static_dash_motion(self, motion: "Motion", new_turns: Turns) -> None:
        """Handle specific logic for static or dash motion types."""
        if new_turns == 0:
            motion.prop_rot_dir = NO_ROT

            self.rot_dir_button_manager.unpress_vtg_buttons()
            self.rot_dir_button_manager.hide_vtg_dir_buttons()

        elif motion.turns == 0:
            self._set_prop_rot_dir_based_on_button_state(motion)

    def _set_prop_rot_dir_based_on_button_state(self, motion: "Motion") -> None:
        """Set the rotation direction of the motion based on the state of either the prop_rot_dir button or the vtg_dir buttons."""
        other_motion = motion.pictograph.get.other_motion(motion)
        motion.prop_rot_dir = self._determine_prop_rot_dir(motion, other_motion)

    def _determine_prop_rot_dir(
        self, motion: "Motion", other_motion: "Motion"
    ) -> PropRotDirs:
        """Determine the property rotation direction."""
        letter = motion.pictograph.letter
        if letter in Type2_letters or letter in Type3_letters:
            same_button_clicked = self.turns_box.vtg_dir_btn_state[SAME]
            opp_button_clicked = self.turns_box.vtg_dir_btn_state[OPP]

            if not same_button_clicked and not opp_button_clicked:
                self._set_vtg_dir_state_default()

            if same_button_clicked:
                return other_motion.prop_rot_dir
            if opp_button_clicked:
                if other_motion.prop_rot_dir == CLOCKWISE:
                    return COUNTER_CLOCKWISE
                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    return CLOCKWISE

        elif letter in Type4_letters:
            cw_button_clicked = self.turns_box.prop_rot_dir_btn_state[CLOCKWISE]
            ccw_button_clicked = self.turns_box.prop_rot_dir_btn_state[
                COUNTER_CLOCKWISE
            ]

            if not cw_button_clicked and not ccw_button_clicked:
                self._set_prop_rot_dir_state_default()

            if cw_button_clicked:
                return CLOCKWISE
            elif ccw_button_clicked:
                return COUNTER_CLOCKWISE

    def _set_vtg_dir_state_default(self) -> None:
        """Set the vtg direction state to default."""
        self.turns_box.vtg_dir_btn_state[SAME] = True
        self.turns_box.vtg_dir_btn_state[OPP] = False
        self.rot_dir_button_manager.same_button.press()

    def _set_prop_rot_dir_state_default(self) -> None:
        """Set the vtg direction state to default."""
        self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
        self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False
        self.rot_dir_button_manager.cw_button.press()

    def _clamp_turns(self, turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))
