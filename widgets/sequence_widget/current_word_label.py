from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class CurrentWordLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.current_word = None

    def resize_current_word_label(self):
        sequence_widget_width = self.sequence_widget.width()
        label_size = sequence_widget_width // 20
        font = self.font()
        font.setPointSize(int(label_size * 0.8))
        self.setFont(font)
        self.setFixedHeight(label_size)
