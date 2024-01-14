from typing import TYPE_CHECKING, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    LEAD_STATE,
    MOTION_TYPE,
    NO_ROT,
    OPP,
    RED,
    SAME,
    STATIC,
)
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from ....attr_box_widgets.base_turns_widget import BaseTurnsWidget
from ....attr_panel.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from ..by_color.ig_color_attr_box import IGColorAttrBox
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox
    from ..by_lead_state.ig_lead_state_attr_box import IGLeadStateAttrBox


class BaseIGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: Union[
            "IGColorAttrBox", "IGMotionTypeAttrBox", "IGLeadStateAttrBox"
        ] = attr_box
        self.initialize_ui()

    def initialize_ui(self) -> None:
        super()._initialize_ui()
        self.create_turns_buttons()
        self.layout_widgets()

    def create_turns_buttons(self) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()
        for value in turns_values:
            button = self.create_button(value)
            self.turns_buttons_layout.addWidget(button)

    def create_button(self, value: str) -> QPushButton:
        button = QPushButton(value, self)
        button.setStyleSheet(self._get_direct_set_button_style_sheet())
        button.setContentsMargins(0, 0, 0, 0)
        button.setMinimumWidth(button.fontMetrics().boundingRect(value).width() + 10)
        button.clicked.connect(lambda _, v=value: self._direct_set_turns(float(v)))
        return button

    def layout_widgets(self) -> None:
        self.turns_buttons_frame = self.create_frame(self.turns_buttons_layout)
        self.layout.addWidget(self.turns_buttons_frame)

    @staticmethod
    def create_frame(layout: QHBoxLayout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        return frame

    def _direct_set_turns(self, new_turns: Union[int, float]) -> None:
        new_turns = int(new_turns) if new_turns.is_integer() else new_turns
        self.update_turns_display(new_turns)
        self.set_turns(new_turns)

    def adjust_turns(self, adjustment: float) -> None:
        """Adjust turns for a given pictograph based on the attribute type."""
        turns = self.turns_display.text()
        turns = self._convert_turns_from_str_to_num(turns)
        turns += adjustment
        if turns < 0:
            turns = 0
        elif turns > 3:
            turns = 3
        turns = str(turns)
        if turns in ["0.0", "1.0", "2.0", "3.0"]:
            turns = turns[:-2]
        self.update_turns_display(turns)
        
        simulate_same_click = self._check_static_motion_with_zero_turns()

        # Simulate button click if necessary
        if simulate_same_click:
            self._simulate_same_button_click()

        for pictograph in self.attr_box.pictographs.values():
            self._adjust_turns_for_pictograph(pictograph, adjustment)

    def _check_static_motion_with_zero_turns(self) -> bool:
        """Check if any static motion with zero turns exists."""
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

    def set_turns(self, new_turns: Union[int, float]) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if self.is_motion_relevant(motion):
                    self.update_motion_properties(motion, new_turns)

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
            elif (
                motion.turns == 0
            ):  # This implies the motion's initial turns were not 0
                self._set_prop_rot_dir_based_on_vtg_state(motion)
                
        motion.set_turns(new_turns)

    def update_pictograph(self, motion: Motion, new_turns: Union[int, float]) -> None:
        pictograph_dict = {f"{motion.color}_turns": new_turns}
        motion.scene.update_pictograph(pictograph_dict)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display.setText(str(turns))

    def _update_vtg_button_states(self, new_turns: Union[int, float]) -> None:
        """Update the states of the vtg buttons based on the new turns."""
        no_rotation = new_turns == 0
        # Assuming `vtg_dir_btn_state` is a dictionary with the keys 'SAME' and 'OPP'
        self.attr_box.vtg_dir_btn_state[SAME] = not no_rotation
        self.attr_box.vtg_dir_btn_state[OPP] = not no_rotation

        if hasattr(self.attr_box, "same_button"):
            self._set_button_style(self.attr_box.same_button, not no_rotation)
            self._set_button_style(self.attr_box.opp_button, not no_rotation)

            if new_turns > 0:
                self._set_button_checked_state(
                    self.attr_box.same_button, self.attr_box.vtg_dir_btn_state[SAME]
                )
                self._set_button_checked_state(
                    self.attr_box.opp_button, self.attr_box.vtg_dir_btn_state[OPP]
                )

    def _set_button_style(self, button: QPushButton, pressed: bool) -> None:
        """Set the style of the button based on whether it's pressed."""
        button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=pressed))

    def _set_button_checked_state(self, button: QPushButton, state: bool) -> None:
        """Set the checked state of the button."""
        button.setChecked(state)
        button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=state))

    def _apply_new_turns_to_motions(self, new_turns: Union[int, float]) -> None:
        """Apply the new turns value to the relevant motions in the pictographs."""
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if self._is_motion_relevant(motion):
                    self._update_motion_properties(motion, new_turns)

    def _update_motion_properties(
        self, motion: Motion, new_turns: Union[int, float]
    ) -> None:
        """Update motion properties based on the new turns value."""
        motion.set_turns(new_turns)
        if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
            motion.prop_rot_dir = NO_ROT
        elif motion.turns == 0 and motion.motion_type in [DASH, STATIC]:
            self.attr_box.vtg_dir_btn_state[SAME] = True
            self._set_prop_rot_dir_based_on_vtg_state(motion)

        self.update_pictograph(motion, new_turns)

    def _is_motion_relevant(self, motion: Motion) -> bool:
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

    def get_vtg_dir_btn_style(self, pressed: bool) -> str:
        """Return the style sheet for the vtg direction buttons."""
        # Assuming there's a method or property in self.attr_box to get the button style
        return self.get_vtg_dir_btn_style(pressed)

    def _simulate_same_button_click(self) -> None:
        """Simulate clicking the 'same' button."""
        if hasattr(self.attr_box, "same_button"):
            self.attr_box.same_button.click()
