from typing import TYPE_CHECKING
from main_window.main_widget.learn_widget.base_classes.base_lesson_widget import (
    BaseLessonWidget,
)
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .Lesson_1_question_widget import Lesson1QuestionWidget
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .lesson_1_question_generator import Lesson1QuestionGenerator

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget, handling pictograph to letter matching."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)

        self.question_widget = Lesson1QuestionWidget(self)
        self.answers_widget = Lesson1AnswersWidget(self)
        self.question_generator = Lesson1QuestionGenerator(self)

        self._setup_layout()

