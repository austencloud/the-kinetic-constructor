from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt, QTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class IndicatorLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.font_size = sequence_widget.width() // 50
        font = self.font()
        font.setPointSize(self.font_size)
        self.setFont(font)
        self.setStyleSheet("color: green;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clear)
        self.setContentsMargins(0, 0, 0, 0)
        # add black border
        # self.setStyleSheet("border: 1px solid black;")

<<<<<<< HEAD
    def show_indicator(self, text):
=======
    def show_message(self, text) -> None:
>>>>>>> 6fa36c8ff84359dfba82ab7ab201d6bca117a409
        self.setText(text)
        self.timer.start(5000)  # 5000 milliseconds = 5 seconds

    def clear(self):
        self.setText(" ")

    def resize_indicator_label(self):
        self.adjustSize()
        height = self.font_size  # Set a fixed height based on font size
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
