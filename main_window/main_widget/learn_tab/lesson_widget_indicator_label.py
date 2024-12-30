from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, pyqtSlot
from typing import TYPE_CHECKING, Union

from main_window.main_widget.base_indicator_label import BaseIndicatorLabel

if TYPE_CHECKING:
    from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class LessonWidgetIndicatorLabel(BaseIndicatorLabel):
    def __init__(self, lesson_widget: "BaseLessonWidget") -> None:
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget

    def resizeEvent(self, event) -> None:
        self.setFixedHeight(self.lesson_widget.height() // 16)
        font = self.font()
        font.setPointSize(self.lesson_widget.width() // 30)
        self.setFont(font)
