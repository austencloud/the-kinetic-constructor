from ..base_classes.base_lesson_widget import BaseLessonWidget
from .lesson_2_question_generator import Lesson2QuestionGenerator
from .lesson_2_question_widget import Lesson2QuestionWidget
from .lesson_2_answers_widget import Lesson2AnswersWidget


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget, handling letter to pictograph matching."""

    def __init__(self, learn_widget) -> None:
        super().__init__(learn_widget)

        self.question_widget = Lesson2QuestionWidget(self)
        self.answers_widget = Lesson2AnswersWidget(self)
        self.question_generator = Lesson2QuestionGenerator(self)

        self._setup_layout()

