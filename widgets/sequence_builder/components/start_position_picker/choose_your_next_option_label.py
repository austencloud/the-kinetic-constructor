from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker import (
        OptionPicker,
    )


class ChooseYourNextOptionLabel(QLabel):
    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.setText("Choose your next option!")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hide()

    def set_stylesheet(self) -> None:
        width = self.option_picker.width()
        font_size = int(0.02 * width)
        self.setFont(QFont("Cambria", font_size))
        self.show()
