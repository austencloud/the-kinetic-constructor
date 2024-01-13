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
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from ....attr_box_widgets.base_turns_widget import BaseTurnsWidget
from ....attr_panel.base_attr_box import BaseAttrBox

if TYPE_CHECKING:
    from ..by_color.ig_color_attr_box import IGColorAttrBox
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox
    from ..by_lead_state.ig_lead_state_attr_box import IGLeadStateAttrBox
    from .ig_color_turns_widget import IGColorTurnsWidget
    from .ig_lead_state_turns_widget import IGLeadStateTurnsWidget
    from .ig_motion_type_turns_widget import IGMotionTypeTurnsWidget


class BaseIGTurnsWidget(BaseTurnsWidget):
    def __init__(
        self,
        attr_box: Union["IGMotionTypeAttrBox", "IGLeadStateAttrBox", "IGColorAttrBox"],
    ) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box

        self._initialize_ui()
        self.setup_direct_set_turns_buttons()

    def setup_direct_set_turns_buttons(self) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()  # Create a horizontal layout
        button_style_sheet = self._get_direct_set_button_style_sheet()

        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.setContentsMargins(0, 0, 0, 0)
            button.setMinimumWidth(
                button.fontMetrics().boundingRect(value).width() + 10
            )
            button.clicked.connect(
                lambda checked, v=value: self._direct_set_turns(float(v))
            )
            self.turns_buttons_layout.addWidget(button)

        self.turns_buttons_frame = QFrame(self)
        self.turns_buttons_frame.setLayout(self.turns_buttons_layout)

        self.turns_buttons_frame.setContentsMargins(0, 0, 0, 0)
        self.turns_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.turns_buttons_layout.setSpacing(0)
        self.layout.addWidget(self.turns_buttons_frame)

    def adjust_turns(self, pictograph: Pictograph, adjustment: float) -> None:
        """Adjust turns for a given pictograph based on the AttrBox's attribute type."""
        new_turns = None
        for motion in pictograph.motions.values():
            if self.attr_box.attribute_type == MOTION_TYPE:
                if motion.motion_type == self.attr_box.motion_type:
                    self.process_turns_adjustment_for_single_motion(motion, adjustment)
                    if new_turns is None:
                        new_turns = motion.turns
            elif self.attr_box.attribute_type == COLOR:
                if motion.color == self.attr_box.color:
                    self.process_turns_adjustment_for_single_motion(motion, adjustment)
                    if new_turns is None:
                        new_turns = motion.turns
            elif self.attr_box.attribute_type == LEAD_STATE:
                if motion.lead_state == self.attr_box.lead_state:
                    self.process_turns_adjustment_for_single_motion(motion, adjustment)
                    if new_turns is None:
                        new_turns = motion.turns

        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        self.update_turns_display(new_turns)

    def create_frame(self) -> QFrame:
        frame = QFrame()
        frame.setContentsMargins(0, 0, 0, 0)
        return frame

    def are_pictographs_with_dash_or_static_motion_in_scroll_area(
        self,
    ) -> bool:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    return True
        return False

    def _direct_set_turns(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        new_turns: Union[int, float],
    ) -> None:
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)
        
        if hasattr(self.attr_box, "same_button"):
            self.vtg_dir_btn_state = self.attr_box.vtg_dir_btn_state
            if self.attr_box.attribute_type == MOTION_TYPE:
            
                if self.are_pictographs_with_dash_or_static_motion_in_scroll_area():
                    if new_turns == 0:
                        self.attr_box.same_button.setStyleSheet(
                            self.get_vtg_dir_btn_style(pressed=False)
                        )
                        self.attr_box.opp_button.setStyleSheet(
                            self.get_vtg_dir_btn_style(pressed=False)
                        )

                    elif new_turns > 0:
                        self.attr_box.same_button.setChecked(self.vtg_dir_btn_state[SAME])
                        self.attr_box.opp_button.setChecked(self.vtg_dir_btn_state[OPP])
                        self.attr_box.same_button.setStyleSheet(
                            self.get_vtg_dir_btn_style(
                                pressed=(self.vtg_dir_btn_state[SAME])
                            )
                        )
                        self.attr_box.opp_button.setStyleSheet(
                            self.get_vtg_dir_btn_style(
                                pressed=(self.vtg_dir_btn_state[OPP])
                            )
                        )

        # Apply new turns to motions
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = pictograph.get_other_motion(motion)
                if self.attr_box.attribute_type == MOTION_TYPE:
                    if motion.motion_type == self.attr_box.motion_type:
                        if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
                            motion.prop_rot_dir = NO_ROT
                        if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                            if self.vtg_dir_btn_state[SAME]:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                            elif self.vtg_dir_btn_state[OPP]:
                                if other_motion.prop_rot_dir == CLOCKWISE:
                                    motion.prop_rot_dir = COUNTER_CLOCKWISE
                                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                                    motion.prop_rot_dir = CLOCKWISE
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                        pictograph.update_pictograph(pictograph_dict)

                elif self.attr_box.attribute_type == COLOR:
                    if motion.color == self.attr_box.color:
                        if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
                            motion.prop_rot_dir = NO_ROT
                        if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                            if self.vtg_dir_btn_state[SAME]:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                            elif self.vtg_dir_btn_state[OPP]:
                                if other_motion.prop_rot_dir == CLOCKWISE:
                                    motion.prop_rot_dir = COUNTER_CLOCKWISE
                                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                                    motion.prop_rot_dir = CLOCKWISE
                            else:
                                motion.prop_rot_dir = NO_ROT
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                        pictograph.update_pictograph(pictograph_dict)

    def process_turns_adjustment_for_single_motion(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        motion: Motion,
        adjustment: float,
    ) -> None:
        other_motion = motion.scene.motions[RED if motion.color == BLUE else BLUE]

        new_turns = self._calculate_new_turns(motion.turns, adjustment)
        if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
            motion.prop_rot_dir = NO_ROT
            for button in self.attr_box.same_opp_buttons:
                button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=False))
        simulate_same_click = False

        if new_turns > 0 and motion.motion_type in [DASH, STATIC]:
            if motion.turns == 0:
                simulate_same_click = True
                motion.prop_rot_dir = other_motion.prop_rot_dir
            if simulate_same_click:
                if (
                    not self.attr_box.same_button.isChecked()
                    and not self.attr_box.opp_button.isChecked()
                ):
                    self._simulate_same_button_click()

        motion.set_turns(new_turns)
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def _calculate_new_turns(self, current_turns, adjustment):
        new_turns = max(0, min(3, current_turns + adjustment))
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        return new_turns

    ### EVENT HANDLERS ###

    def update_ig_turnbox_size(self) -> None:
        """Update the size of the turns display for motion type."""
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = (
            min(self.turns_display.width(), self.turns_display.height()) * 0.25
        )
        box_font_size = int(self.attr_box.width() / 14)

        self.turns_display.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turns_display.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turns_display.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turns_display.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_display.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

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

    def update_turns_display(
        self: Union[
            "IGMotionTypeTurnsWidget", "IGLeadStateTurnsWidget", "IGColorTurnsWidget"
        ],
        turns: Union[int, float],
    ) -> None:
        """Update the turns display based on the latest turns value."""
        self.turns_display.setText(str(turns))

    def calculate_turns_button_size(self) -> int:
        return int(self.attr_box.width() / 10)

    def resize_turns_widget(self) -> None:
        self.update_ig_turnbox_size()
        self.update_adjust_turns_button_size()

    def update_adjust_turns_button_size(self) -> None:
        for button in self.adjust_turns_buttons:
            button_size = self.calculate_adjust_turns_button_size()
            button.update_attr_box_adjust_turns_button_size(button_size)

    def calculate_adjust_turns_button_size(self) -> int:
        return int(self.attr_box.height() / 6)
