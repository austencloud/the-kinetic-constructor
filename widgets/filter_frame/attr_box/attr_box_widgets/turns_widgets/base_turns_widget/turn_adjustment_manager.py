from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QFrame
from typing import TYPE_CHECKING, List, Union
from constants import *
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from ...attr_box_button import AdjustTurnsButton

if TYPE_CHECKING:
    from ..base_turns_widget.base_turns_widget import BaseTurnsWidget
    from ......filter_frame.attr_box.color_attr_box import ColorAttrBox
    from ......filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox
    from ......filter_frame.attr_box.lead_state_attr_box import LeadStateAttrBox


class AdjustTurnsManager:
    def __init__(self, attr_box, parent_widget: "BaseTurnsWidget") -> None:
        self.attr_box: Union[
            "ColorAttrBox", "MotionTypeAttrBox", "LeadStateAttrBox"
        ] = attr_box
        self.parent_widget = parent_widget

    def setup_adjustment_buttons(self) -> None:
        self.negative_buttons_frame = QFrame()
        self.positive_buttons_frame = QFrame()
        self.negative_buttons_layout = QVBoxLayout(self.negative_buttons_frame)
        self.positive_buttons_layout = QVBoxLayout(self.positive_buttons_frame)
        """Create and setup adjustment buttons."""
        adjustments = [(-1, "-1"), (-0.5, "-0.5"), (0.5, "+0.5"), (1, "+1")]
        self.adjust_turns_buttons = []

        for adjustment, text in adjustments:
            button = self.create_adjust_turns_button(text)

            button.clicked.connect(lambda _, adj=adjustment: self.adjust_turns(adj))
            if adjustment < 0:
                self.negative_buttons_layout.addWidget(button)
            else:
                self.positive_buttons_layout.addWidget(button)
            self.adjust_turns_buttons.append(button)

    def create_adjust_turns_button(self, text: str) -> QPushButton:
        button = AdjustTurnsButton(self.parent_widget, text)
        button.setContentsMargins(0, 0, 0, 0)
        button.setMinimumWidth(button.fontMetrics().boundingRect(text).width() + 10)
        return button



    def adjust_turns(self, adjustment: float) -> None:
        """Adjust turns for a given pictograph based on the attribute type."""
        turns = self.parent_widget.turn_display_manager.turns_display.text()
        turns = self.parent_widget._convert_turns_from_str_to_num(turns)
        turns += adjustment
        if turns < 0:
            turns = 0
        elif turns > 3:
            turns = 3
        turns = str(turns)
        if turns in ["0.0", "1.0", "2.0", "3.0"]:
            turns = turns[:-2]
        self.parent_widget.turn_display_manager.update_turns_display(turns)

        simulate_same_click = self._check_dash_static_motion_with_zero_turns()

        # Simulate button click if necessary
        if simulate_same_click:
            self._simulate_same_button_click()

        for pictograph in self.attr_box.pictographs.values():
            self._adjust_turns_for_pictograph(pictograph, adjustment)

    def _check_dash_static_motion_with_zero_turns(self) -> bool:
        """Check if any dash or static motion with zero turns exists."""
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                    return True
        return False

    def _simulate_same_button_click(self) -> None:
        """Simulate clicking the 'same' button."""
        if hasattr(self.attr_box, "same_button"):
            self.attr_box.same_button.click()
            # Assuming there's a method to update the button's stylesheet
            self.update_button_stylesheet(self.attr_box.same_button, pressed=True)

    def update_button_stylesheet(self, button: QPushButton, pressed: bool) -> None:
        """Update the stylesheet of a button based on whether it's pressed."""
        if pressed:
            # Assuming there is a predefined style for pressed buttons
            button.setStyleSheet(self.get_pressed_button_style())
        else:
            # Assuming there is a predefined style for unpressed buttons
            button.setStyleSheet(self.get_unpressed_button_style())

    def get_pressed_button_style(self) -> str:
        """Return the stylesheet for a pressed button."""
        # Placeholder for the actual stylesheet
        return "QPushButton { background-color: #cccccc; }"

    def get_unpressed_button_style(self) -> str:
        """Return the stylesheet for an unpressed button."""
        # Placeholder for the actual stylesheet
        return "QPushButton { background-color: #ffffff; }"

    def _adjust_turns_for_pictograph(
        self, pictograph: Pictograph, adjustment: float
    ) -> None:
        """Adjust turns for each relevant motion in the pictograph."""
        for motion in pictograph.motions.values():
            if self.is_motion_relevant(motion):
                new_turns = self._calculate_new_turns(motion.turns, adjustment)
                self.update_motion_properties(motion, new_turns)

    def _calculate_new_turns(self, current_turns: float, adjustment: float) -> float:
        """Calculate new turns value based on adjustment."""
        new_turns = max(0, min(3, current_turns + adjustment))
        return int(new_turns) if new_turns in [0.0, 1.0, 2.0, 3.0] else new_turns

    def is_motion_relevant(self, motion: Motion) -> bool:
        attr_type = self.attr_box.attribute_type
        return getattr(motion, attr_type) == getattr(self.attr_box, attr_type)

    def update_motion_properties(
        self, motion: Motion, new_turns: Union[int, float]
    ) -> None:
        self._update_turns_and_rotation(motion, new_turns)
        self.update_pictograph(motion, new_turns)

    def _update_turns_and_rotation(
        self, motion: Motion, new_turns: Union[int, float]
    ) -> None:
        if motion.motion_type in [DASH, STATIC]:
            if new_turns == 0:
                motion.prop_rot_dir = NO_ROT
                self.unpress_vtg_buttons()
            elif motion.turns == 0:
                self._set_prop_rot_dir_based_on_vtg_state(motion)

        motion.set_motion_turns(new_turns)

    def update_pictograph(self, motion: Motion, new_turns: Union[int, float]) -> None:
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.scene.update_pictograph(pictograph_dict)

    def unpress_vtg_buttons(self) -> None:
        """Unpress the vtg buttons."""
        if hasattr(self.attr_box, "same_button"):
            self.attr_box.same_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
            )
            self.attr_box.opp_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
            )

    def is_motion_relevant(self, motion: Motion) -> bool:
        """Check if a motion is relevant based on the attribute type of the attr_box."""
        return (
            (
                self.attr_box.attribute_type == MOTION_TYPE
                and motion.motion_type == self.attr_box.motion_type
            )
            or (
                self.attr_box.attribute_type == COLOR
                and motion.color == self.attr_box.color
            )
            or (
                self.attr_box.attribute_type == LEAD_STATE
                and motion.lead_state == self.attr_box.lead_state
            )
        )

    def _set_prop_rot_dir_based_on_vtg_state(self, motion: Motion) -> None:
        """Set the rotation direction of the motion based on the vtg directional relationship."""
        other_motion = motion.scene.motions[RED if motion.color == BLUE else BLUE]
        if (
            not self.attr_box.vtg_dir_btn_state[SAME]
            and not self.attr_box.vtg_dir_btn_state[OPP]
        ):
            motion.prop_rot_dir = other_motion.prop_rot_dir
            self.attr_box.vtg_dir_btn_state[SAME] = True
            self.attr_box.vtg_dir_btn_state[OPP] = False
            self.attr_box.same_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=True)
            )
            self.attr_box.opp_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=False)
            )
        if self.attr_box.vtg_dir_btn_state[SAME]:
            motion.prop_rot_dir = other_motion.prop_rot_dir
            self.attr_box.same_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=True)
            )
        elif self.attr_box.vtg_dir_btn_state[OPP]:
            motion.prop_rot_dir = (
                COUNTER_CLOCKWISE
                if other_motion.prop_rot_dir == CLOCKWISE
                else CLOCKWISE
            )
            self.attr_box.opp_button.setStyleSheet(
                self.attr_box.header_widget.get_vtg_dir_btn_style(pressed=True)
            )

    def update_pictograph(self, motion: Motion, new_turns: Union[int, float]) -> None:
        """Update the pictograph with the new turns value."""
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.scene.update_pictograph(pictograph_dict)

    def set_turns(self, new_turns: Union[int, float]) -> None:
        self.parent_widget.turn_display_manager.update_turns_display(new_turns)
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if self.is_motion_relevant(motion):
                    self.update_motion_properties(motion, new_turns)