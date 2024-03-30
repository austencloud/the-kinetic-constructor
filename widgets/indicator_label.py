from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class IndicatorLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.font_size = sequence_widget.width() // 40
        font = self.font()
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.setStyleSheet("color: black;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clear)
        self.setContentsMargins(0, 0, 0, 0)

    def show_indicator(self, text) -> None:
        self.setText(text)
        print(text)
        self.timer.start(5000)

    def clear(self) -> None:
        self.setText(" ")

    def resize_indicator_label(self) -> None:
        self.adjustSize()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
