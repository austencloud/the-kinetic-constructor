from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import BLUE, RED

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_variation_dialog import (
        StartPosVariationDialog,
    )


class StartPosVariationDialogOriChanger(QWidget):
    ori_changed = pyqtSignal(str, str)

    def __init__(self, variation_dialog: "StartPosVariationDialog") -> None:
        super().__init__(variation_dialog)
        self.variation_dialog = variation_dialog
        self.current_ori_index = {RED: 0, BLUE: 0}
        self.orientations = ["in", "counter", "out", "clock"]
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.left_ori_label = QLabel("Left Start Orientation")
        self.right_ori_label = QLabel("Right Start Orientation")
        self.left_current_ori_display = QLabel(
            self.orientations[self.current_ori_index[BLUE]]
        )
        self.right_current_ori_display = QLabel(
            self.orientations[self.current_ori_index[RED]]
        )
        self.left_cw_button = QPushButton(QIcon("path/to/cw_icon.png"), "")
        self.left_ccw_button = QPushButton(QIcon("path/to/ccw_icon.png"), "")
        self.right_cw_button = QPushButton(QIcon("path/to/cw_icon.png"), "")
        self.right_ccw_button = QPushButton(QIcon("path/to/ccw_icon.png"), "")
        self.setup_layout()
        self.connect_signals()

    def setup_layout(self) -> None:
        self.layout.addWidget(self.left_ori_label)
        self.layout.addWidget(self.left_current_ori_display)
        left_button_layout = QHBoxLayout()
        left_button_layout.addWidget(self.left_ccw_button)
        left_button_layout.addWidget(self.left_cw_button)
        self.layout.addLayout(left_button_layout)

        self.layout.addWidget(self.right_ori_label)
        self.layout.addWidget(self.right_current_ori_display)
        right_button_layout = QHBoxLayout()
        right_button_layout.addWidget(self.right_ccw_button)
        right_button_layout.addWidget(self.right_cw_button)
        self.layout.addLayout(right_button_layout)

    def connect_signals(self) -> None:
        self.left_cw_button.clicked.connect(lambda: self.rotate_cw(BLUE))
        self.left_ccw_button.clicked.connect(lambda: self.rotate_ccw(BLUE))
        self.right_cw_button.clicked.connect(lambda: self.rotate_cw(RED))
        self.right_ccw_button.clicked.connect(lambda: self.rotate_ccw(RED))
        self.ori_changed.connect(self.variation_dialog.on_ori_changed)

    def rotate_cw(self, color: Color) -> None:
        self.current_ori_index[color] = (self.current_ori_index[color] + 1) % len(
            self.orientations
        )
        self.update_display(color)

    def rotate_ccw(self, color: Color) -> None:
        self.current_ori_index[color] = (self.current_ori_index[color] - 1) % len(
            self.orientations
        )
        self.update_display(color)

    def update_display(self, color: Color) -> None:
        new_ori = self.orientations[self.current_ori_index[color]]
        if color == BLUE:
            self.left_current_ori_display.setText(new_ori)
        else:
            self.right_current_ori_display.setText(new_ori)
        self.ori_changed.emit(new_ori, color)

    def set_orientation(self, color: Color, orientation: str) -> None:
        self.current_ori_index[color] = self.orientations.index(orientation)
        self.update_display(color)