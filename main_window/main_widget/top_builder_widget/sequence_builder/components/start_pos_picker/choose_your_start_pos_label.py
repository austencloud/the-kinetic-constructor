from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union




if TYPE_CHECKING:
    from ...advanced_start_pos_picker.advanced_start_pos_picker import AdvancedStartPosPicker
    from ...components.start_pos_picker.start_pos_picker import StartPosPicker


class ChooseYourStartPosLabel(QLabel):
    def __init__(self, start_pos_picker: Union["StartPosPicker", "AdvancedStartPosPicker"]) -> None:
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.setText("Choose your start position!")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setGeometry(0, 0, self.start_pos_picker.width(), 50)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

    def set_stylesheet(self) -> None:
        width = self.start_pos_picker.width()
        font_size = int(0.04 * width)
        self.setFont(QFont("Monotype Corsiva", font_size))
        self.show()

