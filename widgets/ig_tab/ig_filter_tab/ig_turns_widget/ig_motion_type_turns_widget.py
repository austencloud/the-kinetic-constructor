from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    LEAD_STATE,
    MOTION_TYPE,
    NO_ROT,
    OPP,
    RED,
    SAME,
    STATIC,
)
from objects.pictograph.pictograph import Pictograph
from .base_ig_turns_widget import BaseIGTurnsWidget

if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGMotionTypeAttrBox") -> None:
        """Initialize the IGMotionTypeTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.dash_button_state = {SAME: True, OPP: False}
        self.static_button_state = {SAME: True, OPP: False}

        if self.attr_box.motion_type in [DASH, STATIC]:
            self.same_button = self.attr_box.header_widget.same_button
            self.opp_button = self.attr_box.header_widget.opp_button


    def _direct_set_turns_by_motion_type(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)
        if self.attr_box.motion_type in [DASH, STATIC]:
            if new_turns == 0:
                # Save the state before deselecting buttons
                if self.attr_box.motion_type == DASH:
                    self.dash_button_state[SAME] = self.same_button.isChecked()
                    self.dash_button_state[OPP] = self.opp_button.isChecked()
                elif self.attr_box.motion_type == STATIC:
                    self.static_button_state[SAME] = self.same_button.isChecked()
                    self.static_button_state[OPP] = self.opp_button.isChecked()

                # Deselect buttons
                self.same_button.setChecked(False)
                self.opp_button.setChecked(False)
                self.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_button_style(pressed=False)
                )
                self.opp_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_button_style(pressed=False)
                )

            elif new_turns > 0:
                if self.attr_box.motion_type == DASH and not (
                    self.dash_button_state[SAME] or self.dash_button_state[OPP]
                ):
                    # self.same_button.setChecked(True)
                    self.opp_button.setChecked(False)
                    self.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=True
                        )
                    )
                elif self.attr_box.motion_type == STATIC and not (
                    self.static_button_state[SAME] or self.static_button_state[OPP]
                ):
                    self.same_button.setChecked(True)
                else:
                    # Apply the saved state
                    self.same_button.setChecked(
                        self.dash_button_state[SAME]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[SAME]
                    )
                    self.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=(
                                self.dash_button_state[SAME]
                                if self.attr_box.motion_type == DASH
                                else self.static_button_state[SAME]
                            )
                        )
                    )
                    self.opp_button.setChecked(
                        self.dash_button_state[OPP]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[OPP]
                    )
                    self.opp_button.setStyleSheet(
                        self.attr_box.header_widget.get_vtg_dir_button_style(
                            pressed=(
                                self.dash_button_state[OPP]
                                if self.attr_box.motion_type == DASH
                                else self.static_button_state[OPP]
                            )
                        )
                    )

        # Apply new turns to motions
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[RED if motion.color == BLUE else BLUE]

                if motion.motion_type == self.attr_box.motion_type:
                    if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
                        motion.prop_rot_dir = NO_ROT
                    if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                        if self.same_button.isChecked():
                            motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.opp_button.isChecked():
                            if other_motion.prop_rot_dir is CLOCKWISE:
                                motion.prop_rot_dir = COUNTER_CLOCKWISE
                            elif other_motion.prop_rot_dir is COUNTER_CLOCKWISE:
                                motion.prop_rot_dir = CLOCKWISE
                    pictograph_dict = {
                        f"{motion.color}_turns": new_turns,
                    }
                    pictograph.update_pictograph(pictograph_dict)

    def update_turns_display_for_pictograph(self, pictograph: Pictograph) -> None:
        """Update the turnbox display based on the latest turns value of the pictograph."""
        for motion in pictograph.get_motions_by_type(self.attr_box.motion_type):
            self.update_turns_display(motion.turns)
            break

    def _update_turns_directly_by_motion_type(self, turns: str) -> None:
        turns = self._convert_turns_from_str_to_num(turns)
        self._direct_set_turns_by_motion_type(turns)

    def resize_turns_widget(self) -> None:
        self.update_turnbox_size()
        self.update_adjust_turns_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        simulate_same_click = False

        # Check if any static motion with zero turns exists
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if (
                    motion.motion_type in [DASH, STATIC]
                    and motion.turns == 0
                    and motion.motion_type == self.attr_box.motion_type
                ):
                    simulate_same_click = True
                    break
            if simulate_same_click:
                break

        # Simulate CW button click if necessary
        if simulate_same_click:
            if hasattr(self.attr_box.header_widget, "same_button"):
                if not self.same_button.isChecked() and not self.opp_button.isChecked():
                    self._simulate_same_button_click()
                # set the stylesheet to pressed
                self.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_vtg_dir_button_style(pressed=True)
                )

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                    other_motion = pictograph.motions[
                        RED if motion.color == BLUE else BLUE
                    ]
                    if hasattr(self.attr_box.header_widget, "same_button"):
                        if self.same_button.isChecked():
                            if other_motion.prop_rot_dir:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.opp_button.isChecked():
                            if other_motion.prop_rot_dir is CLOCKWISE:
                                motion.prop_rot_dir = COUNTER_CLOCKWISE
                            elif other_motion.prop_rot_dir is COUNTER_CLOCKWISE:
                                motion.prop_rot_dir = CLOCKWISE

        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns(pictograph, adjustment)

    def _simulate_same_button_click(self):
        self.same_button.setChecked(True)
        self.opp_button.setChecked(False)
        self.same_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_button_style(pressed=True)
        )
        self.opp_button.setStyleSheet(
            self.attr_box.header_widget.get_vtg_dir_button_style(pressed=False)
        )

    def _set_turns(self, new_turns: int | float) -> None:
        self._direct_set_turns_by_motion_type(new_turns)
