from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QSize
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
        self.current_orientation_index = 0
        self.orientations = [IN, OUT, CLOCK, COUNTER]
        self._setup_orientation_label()
        self._setup_orientation_control_layout()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
        )
        self.layout.addWidget(self.ori_label, 1)
        self.layout.addWidget(self.current_orientation_display, 1)
        self.layout.addLayout(self.orientation_control_layout, 4)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def _setup_orientation_label(self):
        self.ori_label = QLabel("Start Orientation")
        self.ori_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _set_ori_label_font_size(self):
        ori_label_font_size = self.ori_picker_box.graph_editor.width() // 50
        font = QFont("Cambria", ori_label_font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.ori_label.setFont(font)

    def _setup_orientation_control_layout(self):
        path = "images/icons"
        self.ccw_button = self.setup_button(f"{path}/rotate_ccw.png", self.rotate_ccw)
        self.current_orientation_display = self.setup_current_orientation_display()
        self.cw_button = self.setup_button(f"{path}/rotate_cw.png", self.rotate_cw)
        self.orientation_control_layout = QHBoxLayout()
        self.orientation_control_layout.addStretch(5)
        self.orientation_control_layout.addWidget(self.ccw_button)
        self.orientation_control_layout.addWidget(self.cw_button)
        self.orientation_control_layout.addStretch(5)

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
        # self.current_orientation_display.setFixedWidth(self.ori_picker_box.width() // 3)
        button_size = int(self.ori_picker_box.calculate_button_size())
        icon_size = int(button_size * 0.6)
        for button in [self.ccw_button, self.cw_button]:
            button.setFixedSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))
        self._set_ori_label_font_size()
