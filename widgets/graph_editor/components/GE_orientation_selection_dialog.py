from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from constants import IN, COUNTER, OUT, CLOCK

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker_widget import (
        GE_StartPosOriPickerWidget,
    )


class GE_OrientationSelectionDialog(QDialog):
    def __init__(self, ori_picker: "GE_StartPosOriPickerWidget"):
        super().__init__(
            ori_picker, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.ori_picker = ori_picker
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Define the orientations
        orientations = [IN, COUNTER, OUT, CLOCK]

        # Create a button for each orientation
        for orientation in orientations:
            button = QPushButton(orientation)
            button.setFont(QFont("Arial", 14))
            button.clicked.connect(
                lambda checked, ori=orientation: self.select_orientation(ori)
            )
            layout.addWidget(button)

    def select_orientation(self, orientation):
        # Emit signal or directly set the orientation in parent widget
        self.ori_picker.set_orientation(orientation)
        self.accept()
