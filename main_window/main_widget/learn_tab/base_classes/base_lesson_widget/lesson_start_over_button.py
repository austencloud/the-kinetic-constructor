from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt




if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonStartOverButton(QPushButton):
    """Custom Start Over button with resize functionality."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__("Start Over")
        self.lesson_widget = lesson_widget
        self.clicked.connect(self.lesson_widget.prepare_quiz_ui)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event):
        font_size = self.lesson_widget.main_widget.width() // 60
        self.setStyleSheet(f"font-size: {font_size}px;")
        self.setFixedSize(
            self.lesson_widget.main_widget.width() // 8,
            self.lesson_widget.main_widget.height() // 12,
        )
