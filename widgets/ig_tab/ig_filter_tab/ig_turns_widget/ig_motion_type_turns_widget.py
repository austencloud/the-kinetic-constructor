from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
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

    def adjust_turns_by_motion_type(
        self, pictograph: Pictograph, adjustment: float
    ) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        new_turns = None
        for motion in pictograph.motions.values():
            if motion.motion_type == self.attr_box.motion_type:
                self.process_turns_adjustment_for_single_motion(motion, adjustment)
                if new_turns is None:
                    new_turns = motion.turns
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        self.update_turns_display(new_turns)

    def _direct_set_turns_by_motion_type(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)
        if self.attr_box.motion_type in [DASH, STATIC]:
            if new_turns == 0:
                # Save the state before deselecting buttons
                if self.attr_box.motion_type == DASH:
                    self.dash_button_state[
                        SAME
                    ] = self.attr_box.header_widget.same_button.isChecked()
                    self.dash_button_state[
                        OPP
                    ] = self.attr_box.header_widget.opp_button.isChecked()
                elif self.attr_box.motion_type == STATIC:
                    self.static_button_state[
                        SAME
                    ] = self.attr_box.header_widget.same_button.isChecked()
                    self.static_button_state[
                        OPP
                    ] = self.attr_box.header_widget.opp_button.isChecked()

                # Deselect buttons
                self.attr_box.header_widget.same_button.setChecked(False)
                self.attr_box.header_widget.opp_button.setChecked(False)
                self.attr_box.header_widget.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_button_style(pressed=False)
                )
                self.attr_box.header_widget.opp_button.setStyleSheet(
                    self.attr_box.header_widget.get_button_style(pressed=False)
                )

            elif new_turns > 0:
                if self.attr_box.motion_type == DASH and not (
                    self.dash_button_state[SAME] or self.dash_button_state[OPP]
                ):
                    # self.attr_box.header_widget.same_button.setChecked(True)
                    self.attr_box.header_widget.opp_button.setChecked(False)
                    self.attr_box.header_widget.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_button_style(pressed=True)
                    )
                elif self.attr_box.motion_type == STATIC and not (
                    self.static_button_state[SAME] or self.static_button_state[OPP]
                ):
                    self.attr_box.header_widget.same_button.setChecked(True)
                else:
                    # Apply the saved state
                    self.attr_box.header_widget.same_button.setChecked(
                        self.dash_button_state[SAME]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[SAME]
                    )
                    self.attr_box.header_widget.same_button.setStyleSheet(
                        self.attr_box.header_widget.get_button_style(
                            pressed=(
                                self.dash_button_state[SAME]
                                if self.attr_box.motion_type == DASH
                                else self.static_button_state[SAME]
                            )
                        )
                    )
                    self.attr_box.header_widget.opp_button.setChecked(
                        self.dash_button_state[OPP]
                        if self.attr_box.motion_type == DASH
                        else self.static_button_state[OPP]
                    )
                    self.attr_box.header_widget.opp_button.setStyleSheet(
                        self.attr_box.header_widget.get_button_style(
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
                        if self.attr_box.header_widget.same_button.isChecked():
                            motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.attr_box.header_widget.opp_button.isChecked():
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

    def update_ig_motion_type_turnbox_size(self) -> None:
        """Update the size of the turns display for motion type."""
        self.spacing = self.attr_box.attr_panel.height() // 250
        border_radius = (
            min(self.turns_display.width(), self.turns_display.height()) * 0.25
        )
        turns_display_font_size = int(self.attr_box.height() / 8)

        self.turns_display.setMinimumHeight(int(self.attr_box.height() / 3))
        self.turns_display.setMaximumHeight(int(self.attr_box.height() / 3))
        self.turns_display.setMinimumWidth(int(self.attr_box.height() / 3))
        self.turns_display.setMaximumWidth(int(self.attr_box.height() / 3))
        self.turns_display.setFont(
            QFont("Arial", turns_display_font_size, QFont.Weight.Bold)
        )

        # Adjust the stylesheet to match the combo box style without the arrow
        self.turns_display.setStyleSheet(
            f"""
            QLabel {{
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def resize_turns_widget(self) -> None:
        self.update_ig_motion_type_turnbox_size()
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
                if (
                    not self.attr_box.header_widget.same_button.isChecked()
                    and not self.attr_box.header_widget.opp_button.isChecked()
                ):
                    self._simulate_same_button_click_in_header_widget()
                # set the stylesheet to pressed
                self.attr_box.header_widget.same_button.setStyleSheet(
                    self.attr_box.header_widget.get_button_style(pressed=True)
                )

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                    other_motion = pictograph.motions[
                        RED if motion.color == BLUE else BLUE
                    ]
                    if hasattr(self.attr_box.header_widget, "same_button"):
                        if self.attr_box.header_widget.same_button.isChecked():
                            if other_motion.prop_rot_dir:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                        elif self.attr_box.header_widget.opp_button.isChecked():
                            if other_motion.prop_rot_dir is CLOCKWISE:
                                motion.prop_rot_dir = COUNTER_CLOCKWISE
                            elif other_motion.prop_rot_dir is COUNTER_CLOCKWISE:
                                motion.prop_rot_dir = CLOCKWISE

        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_by_motion_type(pictograph, adjustment)

    def _simulate_same_button_click_in_header_widget(self):
        self.attr_box.header_widget.same_button.setChecked(True)
        self.attr_box.header_widget.opp_button.setChecked(False)
        self.attr_box.header_widget.same_button.setStyleSheet(
            self.attr_box.header_widget.get_button_style(pressed=True)
        )
        self.attr_box.header_widget.opp_button.setStyleSheet(
            self.attr_box.header_widget.get_button_style(pressed=False)
        )

    def _set_turns(self, new_turns: int | float) -> None:
        self._direct_set_turns_by_motion_type(new_turns)
