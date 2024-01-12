from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import CLOCKWISE, COUNTER_CLOCKWISE, DASH, ICON_DIR, STATIC
from objects.pictograph.pictograph import Pictograph
from .base_ig_turns_widget import BaseIGTurnsWidget

if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGMotionTypeAttrBox") -> None:
        """Initialize the IGMotionTypeTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.update_ig_motion_type_turnbox_size()

    def adjust_turns_by_motion_type(
        self, pictograph: Pictograph, adjustment: float
    ) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        new_turns = None
        for motion in pictograph.get_motions_by_type(self.attr_box.motion_type):
            self.process_turns_adjustment_for_single_motion(motion, adjustment)
            new_turns = motion.turns
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        self.update_turns_display(new_turns)

    def _set_turns_by_motion_type(self, new_turns: Union[int, float]) -> None:
        """Set turns for motions of a specific type to a new value."""
        self.update_turns_display(new_turns)

        # Check if any static motion with zero turns exists
        simulate_cw_click = False
        if self.attr_box.motion_type in [DASH, STATIC]:
            for pictograph in self.attr_box.pictographs.values():
                for motion in pictograph.motions.values():
                    if motion.motion_type == STATIC and motion.turns == 0:
                        simulate_cw_click = True
                        break
                if simulate_cw_click:
                    break

            # Simulate CW button click if necessary
            if simulate_cw_click:
                if (
                    not self.attr_box.header_widget.cw_button.isChecked()
                    and not self.attr_box.header_widget.ccw_button.isChecked()
                ):
                    self._simulate_cw_button_click_in_header_widget()

        # Apply new turns to motions
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    if motion.motion_type == STATIC and motion.turns == 0:
                        if self.attr_box.header_widget.cw_button.isChecked():
                            motion.prop_rot_dir = CLOCKWISE
                        elif self.attr_box.header_widget.ccw_button.isChecked():
                            motion.prop_rot_dir = COUNTER_CLOCKWISE
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
        self._set_turns_by_motion_type(turns)

    def update_ig_motion_type_turnbox_size(self) -> None:
        """Update the size of the turnbox for motion type."""
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 10)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

        self.turnbox.setMinimumHeight(int(self.attr_box.width() / 4))
        self.turnbox.setMaximumHeight(int(self.attr_box.width() / 4))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(QFont("Arial", int(self.width() / 22)))

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turnbox.setStyleSheet(
            f"""
            QComboBox {{
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 0px; /* make room for the arrow on the right */
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_arrow_width}px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* visually separate the arrow part */
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}
            QComboBox::down-arrow {{
                image: url("{ICON_DIR}/combobox_arrow.png");
                width: {int(dropdown_arrow_width * 0.6)}px;
                height: {int(dropdown_arrow_width * 0.6)}px;
            }}
        """
        )

    def resize_turns_widget(self) -> None:
        self.update_ig_motion_type_turnbox_size()
        self.update_add_subtract_button_size()

    def _adjust_turns(self, adjustment) -> None:
        """Adjust turns for a given pictograph based on motion type."""
        simulate_cw_click = False

        # Check if any static motion with zero turns exists
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
                    simulate_cw_click = True
                    break
            if simulate_cw_click:
                break

        # Simulate CW button click if necessary
        if simulate_cw_click:
            if hasattr(self.attr_box.header_widget, "cw_button"):
                if (
                    not self.attr_box.header_widget.cw_button.isChecked()
                    and not self.attr_box.header_widget.ccw_button.isChecked()
                ):
                    self._simulate_cw_button_click_in_header_widget()
        if motion.motion_type in [DASH, STATIC] and motion.turns == 0:
            if self.attr_box.header_widget.cw_button.isChecked():
                motion.prop_rot_dir = CLOCKWISE
            elif self.attr_box.header_widget.ccw_button.isChecked():
                motion.prop_rot_dir = COUNTER_CLOCKWISE
        # Apply adjustment to all relevant motions
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_by_motion_type(pictograph, adjustment)


    def _simulate_cw_button_click_in_header_widget(self):
        # Simulate the CW button click
        self.attr_box.header_widget.cw_button.setChecked(True)
        # self.attr_box.header_widget.cw_button.click()

    def _set_turns(self, new_turns: int | float) -> None:
        self._set_turns_by_motion_type(new_turns)
