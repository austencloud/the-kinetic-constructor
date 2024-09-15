import random
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_widget.base_lesson_widget import BaseLessonWidget
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .Lesson_1_pictograph_container import Lesson1PictographContainer

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


from .lesson_1_answers_widget import Lesson1AnswersWidget


from .lesson_1_question_generator import Lesson1QuestionGenerator


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget, handling pictograph to letter matching."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.question_generator = Lesson1QuestionGenerator(self)
        self.pictograph_viewer = Lesson1PictographContainer(self)
        self.answers_widget = Lesson1AnswersWidget(self)

        # Add specific components for lesson 1
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.question_label)
        self.main_layout.addWidget(self.pictograph_viewer)
        self.main_layout.addWidget(self.answers_widget)
        self.main_layout.addWidget(self.indicator_label)
        self.main_layout.addStretch(3)

    def clear_current_question(self):
        """Clear the current question by resetting viewer and answer buttons."""
        self.pictograph_viewer.clear()
        self.answers_widget.clear()

    def resize_lesson_widget(self):
        self.pictograph_viewer.resize_lesson_1_pictograph_viewer()
        self.answers_widget.resize_lesson_1_answers_widget()
        super().resize_lesson_widget()
