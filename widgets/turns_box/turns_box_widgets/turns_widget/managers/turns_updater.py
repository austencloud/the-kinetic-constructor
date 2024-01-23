from typing import TYPE_CHECKING
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

    def update_motion_properties(self, motion: "Motion", new_turns: Turns) -> None:
        self._update_turns_and_rotation(motion, new_turns)
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _adjust_turns_for_pictograph(
        self, pictograph: "Pictograph", adjustment: Turns
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.motions.values():
            if self.turns_widget.turn_adjust_manager.is_motion_relevant(motion):
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
            self.turns_widget.turn_adjust_manager.unpress_vtg_buttons()
            if hasattr(
                self.turns_widget.turns_box.turns_panel.filter_tab.section,
                "rot_dir_button_manager",
            ):
                self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.hide_vtg_dir_buttons()

        elif motion.turns == 0:
            self._set_prop_rot_dir_based_on_vtg_state(motion)

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
                not self.turns_box.vtg_dir_btn_state[SAME]
                and not self.turns_box.vtg_dir_btn_state[OPP]
            ):
                self._set_vtg_dir_state_default()
                # self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.show_vtg_dir_buttons()
            if self.turns_box.vtg_dir_btn_state[SAME]:
                return other_motion.prop_rot_dir
            if self.turns_box.vtg_dir_btn_state[OPP]:
                if other_motion.prop_rot_dir == CLOCKWISE:
                    return COUNTER_CLOCKWISE
                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    return CLOCKWISE

        elif motion.pictograph.letter in Type4_letters:
            # self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.show_prop_rot_dir_buttons()
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.cw_button.press()
            return CLOCKWISE

    def _set_vtg_dir_state_default(self) -> None:
        """Set the vtg direction state to default."""
        self.turns_box.vtg_dir_btn_state[SAME] = True
        self.turns_box.vtg_dir_btn_state[OPP] = False

    def _clamp_turns(self, turns: Turns) -> Turns:
        """Clamp the turns value to be within allowable range."""
        return max(0, min(3, turns))

    def update_turns_and_visibility(self, motion: "Motion", new_turns: Turns) -> None:
        self._update_turns_and_rotation(motion, new_turns)
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

        # Show/hide VTG direction buttons based on the new turns value
        self._update_vtg_button_visibility(motion, new_turns)

    def _update_vtg_button_visibility(self, motion: "Motion", new_turns: Turns) -> None:
        if new_turns > 0:
            # If turns are added, show the VTG direction buttons
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.show_vtg_dir_buttons()
        elif new_turns == 0:
            # If turns are set to 0, hide the VTG direction buttons
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.hide_buttons()
