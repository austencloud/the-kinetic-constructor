from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .sequence_picker import SequencePicker

class SequencePickerCurrentlyDisplayingLabel(QLabel):
    def __init__(self, sequence_picker: "SequencePicker") -> None:
        super().__init__(sequence_picker)
        self.sequence_picker = sequence_picker
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_message(self, description):
        self.setText(f"Currently displaying {description}.")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.sequence_picker.width() // 65)
        self.setFont(font)
