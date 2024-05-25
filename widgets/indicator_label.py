from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QScrollArea,
    QGraphicsOpacityEffect,
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSlot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class IndicatorLabel(QLabel):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.font_size = sequence_widget.width() // 40
        font = self.font()
        font.setPointSize(self.font_size)
        font.setWeight(QFont.Weight.DemiBold)  # Set the font weight to DemiBold
        self.setFont(font)
        self.setStyleSheet("color: black;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)  # Duration of the fade-out in milliseconds
        self.animation.finished.connect(self.clear)

        self.setContentsMargins(0, 0, 0, 0)

    def show_message(self, text) -> None:
        self.setText(text)
        self.opacity_effect.setOpacity(1)  # Ensure the label is fully visible
        # self.show()
        self.timer.start(5000)  # Show the message for 5 seconds

    @pyqtSlot()
    def start_fade_out(self) -> None:
        self.animation.setStartValue(1)  # Start fully visible
        self.animation.setEndValue(0)  # End fully transparent
        self.animation.start()

    def clear(self) -> None:
        self.setText(" ")
        # self.hide()

    # def resize_indicator_label(self) -> None:
    #     self.setMinimumHeight(self.sequence_widget.height() // 10)
