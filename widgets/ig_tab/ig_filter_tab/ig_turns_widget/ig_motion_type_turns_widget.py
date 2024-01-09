from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    ANTI,
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    PRO,
    RED,
    STATIC,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from .base_ig_turns_widget import BaseIGTurnsWidget

if TYPE_CHECKING:
    from ..by_motion_type.ig_motion_type_attr_box import IGMotionTypeAttrBox


class IGMotionTypeTurnsWidget(BaseIGTurnsWidget):
    def __init__(self, attr_box: "IGMotionTypeAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.setup_directset_turns_buttons()
        self.turnbox.currentIndexChanged.connect(self._update_turns_directly)
        self.connect_signals()

    def adjust_turns_by_motion_type(
        self, pictograph: Pictograph, adjustment: float
    ) -> None:
        for motion in pictograph.get_motions_by_type(self.attr_box.motion_type):
            self.process_turns_adjustment_for_single_motion(motion, adjustment)

    def _simulate_cw_button_click_in_header_widget(self):
        self.attr_box.header_widget.cw_button.setChecked(True)
        self.attr_box.header_widget.cw_button.click()

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.header_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.header_widget.ccw_button.isChecked()
            else NO_ROT
        )

    def _update_pictographs_turns_by_motion_type(self, new_turns):
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    def update_turns_incrementally(self, adjustment) -> None:
        self.turnbox.currentIndexChanged.disconnect(
            self.update_turns_directly_by_motion_type
        )
        for pictograph in self.attr_box.pictographs.values():
            self.adjust_turns_by_motion_type(pictograph, adjustment)
        self.turnbox.currentIndexChanged.connect(
            self.update_turns_directly_by_motion_type
        )

    def update_turns_directly_by_motion_type(self, turns) -> None:
        if turns in ["0", "1", "2", "3"]:
            self.turnbox.setCurrentText(turns)
        elif turns in ["0.5", "1.5", "2.5"]:
            self.turnbox.setCurrentText(turns)
        selected_turns_str = self.turnbox.currentText()
        if not selected_turns_str:
            return

        new_turns = float(selected_turns_str)
        self._update_pictographs_turns_by_motion_type(new_turns)

    def _update_turns_directly(self, new_turns):
        if new_turns in ["0", "1", "2", "3"]:
            new_turns = int(new_turns)
        elif new_turns in ["0.5", "1.5", "2.5"]:
            new_turns = float(new_turns)

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    other_motion = pictograph.motions[
                        RED if motion.color == BLUE else BLUE
                    ]
                    if other_motion.motion_type == self.attr_box.motion_type:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{other_motion.color}_turns": new_turns,
                        }
                        motion.scene.update_pictograph(pictograph_dict)
                    elif other_motion.motion_type != self.attr_box.motion_type:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                        motion.scene.update_pictograph(pictograph_dict)

                    self.turnbox.currentIndexChanged.disconnect(
                        self._update_turns_directly
                    )
                    self.update_turns_display(new_turns)
                    self.turnbox.currentIndexChanged.connect(
                        self._update_turns_directly
                    )

    ### EVENT HANDLERS ###

    def update_turnbox_size(self) -> None:
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

        # self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        # self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

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

    def update_button_size(self) -> None:
        for button in self.turns_buttons:
            button_size = self.calculate_button_size()
            button.update_attr_box_turns_button_size(button_size)

    def calculate_button_size(self) -> int:
        return int(self.attr_box.width() / 5)

    def resize_turns_widget(self) -> None:
        self.update_turnbox_size()
        self.update_button_size()

    def setup_directset_turns_buttons(self) -> None:
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()
        button_style_sheet = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #c0c0c0;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #e5e5e5;
            border-color: #a0a0a0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """
        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.clicked.connect(
                lambda checked, v=value: self._update_turns_directly(v)
            )
            self.turns_buttons_layout.addWidget(button)
        self.layout.addLayout(self.turns_buttons_layout)

    def connect_signals(self) -> None:
        self.turnbox.currentIndexChanged.connect(
            self.update_turns_directly_by_motion_type
        )
