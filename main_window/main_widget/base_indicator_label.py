from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSlot
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget




class BaseIndicatorLabel(QLabel):
    def __init__(self, parent_widget: Union["BaseLessonWidget", "SequenceWidget"]) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.font_size = parent_widget.width() // 40
        font = self.font()
        font.setPointSize(self.font_size)
        font.setWeight(QFont.Weight.DemiBold)
        self.setFont(font)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self.clear()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_fade_out)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(2000)
        self.animation.finished.connect(self.clear)

        self.setContentsMargins(0, 0, 0, 0)

    def show_message(self, text) -> None:
        self.timer.stop()
        self.animation.stop()
        self.opacity_effect.setOpacity(1)

        self.setText(text)
        self.timer.start(1000)

    @pyqtSlot()
    def start_fade_out(self) -> None:
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()

    def clear(self) -> None:
        self.setText(" ")

