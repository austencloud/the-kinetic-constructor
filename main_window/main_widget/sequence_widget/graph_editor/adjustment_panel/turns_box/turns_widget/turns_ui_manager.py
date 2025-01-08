class TurnsUIManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.prop_rot_dir_manager = turns_widget.turns_box.prop_rot_dir_button_manager

    def update_turns_display(self, motion: "Motion", new_turns: Turns) -> None:
        """Update the turns display in the UI."""
        self.turns_widget.display_frame.update_turns_display(motion, new_turns)

    def manage_prop_rotation_buttons(self, motion: "Motion", new_turns: Turns) -> None:
        """Manage prop rotation direction buttons based on the new turns value."""
        if new_turns == 0:
            self._handle_zero_turns(motion)
        elif new_turns == "fl":
            self._handle_float_turn_buttons(motion)
        elif new_turns > 0:
            self._handle_positive_turns(motion)

    def _handle_zero_turns(self, motion: "Motion") -> None:
        """Handle button states when turns are zero."""
        if motion.motion_type in [DASH, STATIC]:
            motion.prop_rot_dir = NO_ROT
            self.prop_rot_dir_manager.unpress_prop_rot_dir_buttons()
            self.prop_rot_dir_manager.hide_prop_rot_dir_buttons()
        elif motion.motion_type in [PRO, ANTI]:
            self.prop_rot_dir_manager.show_prop_rot_dir_buttons()

    def _handle_float_turn_buttons(self, motion: "Motion") -> None:
        """Handle button states when turns are 'float'."""
        self.prop_rot_dir_manager.unpress_prop_rot_dir_buttons()
        self.prop_rot_dir_manager.hide_prop_rot_dir_buttons()
        motion.motion_type = FLOAT
        motion.prop_rot_dir = NO_ROT

    def _handle_positive_turns(self, motion: "Motion") -> None:
        """Handle button states when turns are positive."""
        self.prop_rot_dir_manager.show_prop_rot_dir_buttons()
        if motion.prop_rot_dir == NO_ROT:
            motion.prop_rot_dir = CLOCKWISE
            self.prop_rot_dir_manager.cw_button.press()
