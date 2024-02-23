from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt
from constants import IN, OUT, CLOCK, COUNTER
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker_box import (
        GE_StartPosOriPickerBox,
    )


class GE_StartPosOriPickerWidget(QWidget):
    def __init__(self, ori_picker_box: "GE_StartPosOriPickerBox"):
        super().__init__()
        self.ori_picker_box = ori_picker_box
        self.current_orientation_index = (
            0  # Assuming 0 is the default orientation index
        )
        self.orientations = [IN, OUT, CLOCK, COUNTER]
        self.setup_ui()

    def setup_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setup_orientation_label()
        self.setup_orientation_control_layout()
        self.setLayout(self.layout)

    def setup_orientation_label(self):
        self.orientation_label = QLabel("Start Orientation")
        self.orientation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orientation_label.setFont(QFont("Cambria", 16, QFont.Weight.Bold))
        self.layout.addWidget(self.orientation_label)

    def setup_orientation_control_layout(self):
        path = "images/icons"
        self.ccw_button = self.setup_button(f"{path}/rotate_ccw.png", self.rotate_ccw)
        self.current_orientation_display = self.setup_current_orientation_display()
        self.cw_button = self.setup_button(f"{path}/rotate_cw.png", self.rotate_cw)

        self.orientation_control_layout = QHBoxLayout()
        self.orientation_control_layout.addStretch(5)
        self.orientation_control_layout.addWidget(self.ccw_button)
        self.orientation_control_layout.addStretch(1)
        self.orientation_control_layout.addWidget(self.current_orientation_display)
        self.orientation_control_layout.addStretch(1)
        self.orientation_control_layout.addWidget(self.cw_button)
        self.orientation_control_layout.addStretch(5)
        self.layout.addLayout(self.orientation_control_layout)

    def setup_button(self, icon_path, click_function):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(click_function)
        button.setFixedSize(40, 40)
        return button

    def setup_current_orientation_display(self):
        self.current_orientation_display = QLabel(
            self.orientations[self.current_orientation_index]
        )
        self.current_orientation_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_orientation_display.setFont(
            QFont("Cambria", 20, QFont.Weight.Bold)
        )
        # set fixed width to 1/3 the width of ori picker box
        self.current_orientation_display.setFixedWidth(self.ori_picker_box.width() // 3)
        return self.current_orientation_display

    def rotate_cw(self):
        self.current_orientation_index = (self.current_orientation_index + 1) % len(
            self.orientations
        )
        self.current_orientation_display.setText(
            self.orientations[self.current_orientation_index]
        )

    def rotate_ccw(self):
        self.current_orientation_index = (self.current_orientation_index - 1) % len(
            self.orientations
        )
        self.current_orientation_display.setText(
            self.orientations[self.current_orientation_index]
        )

    def resize_GE_start_pos_ori_picker_widget(self):
        self.current_orientation_display.setFixedWidth(self.ori_picker_box.width() // 3)
        for button in [self.ccw_button, self.cw_button]:
            button.setFixedSize(self.ori_picker_box.calculate_button_size())
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
