from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_picker import (
        StartPosPicker,
    )


class ChooseYourStartPositionLabel(QLabel):
    def __init__(self, start_pos_picker: "StartPosPicker") -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.setText("Choose your start position!")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setGeometry(0, 0, self.start_pos_picker.width(), 50)
        self.hide()

    def set_stylesheet(self) -> None:
        width = self.start_pos_picker.width()
        font_size = int(0.03 * width)
        self.setFont(QFont("Monotype Corsiva", font_size))
        # self.setStyleSheet("QLabel { border: 1px solid black; }")
        self.show()
