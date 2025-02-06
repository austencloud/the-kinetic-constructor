from ..base_classes.base_lesson_widget.base_lesson_widget import BaseLessonWidget
from .lesson_2_question_widget import Lesson2QuestionWidget
from .lesson_2_answers_widget import Lesson2AnswersWidget
from .lesson_2_question_generator import Lesson2QuestionGenerator


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget for handling letter to pictograph matching and quiz logic."""

    def __init__(self, learn_widget):
        super().__init__(learn_widget)

        # Override question and answer widgets
        self.question_widget = Lesson2QuestionWidget(self)
        self.answers_widget = Lesson2AnswersWidget(self)
        self.question_generator = Lesson2QuestionGenerator(self)

        # Set up the layout
        # self._setup_layout()
