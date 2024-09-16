from ..base_classes.base_lesson_widget import BaseLessonWidget
from .lesson_3_question_generator import Lesson3QuestionGenerator
from .lesson_3_question_widget import Lesson3QuestionWidget
from .lesson_3_answers_widget import Lesson3AnswersWidget


class Lesson3Widget(BaseLessonWidget):
    """Lesson 3 widget, handling letter to pictograph matching."""

    def __init__(self, learn_widget) -> None:
        super().__init__(learn_widget)

        self.question_widget = Lesson3QuestionWidget(self)
        self.answers_widget = Lesson3AnswersWidget(self)
        self.question_generator = Lesson3QuestionGenerator(self)

        self._setup_layout()
