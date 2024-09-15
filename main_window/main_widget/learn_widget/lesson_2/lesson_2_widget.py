from ..base_lesson_widget import BaseLessonWidget
from .lesson_2_answers_generator import Lesson2AnswersGenerator
from .lesson_2_question_generator import Lesson2QuestionGenerator
from .lesson_2_question_widget import Lesson2QuestionWidget
from .lesson_2_answers_widget import Lesson2AnswersWidget


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget, handling letter to pictograph matching."""

    def __init__(self, learn_widget):
        super().__init__(learn_widget)

        self.question_widget = Lesson2QuestionWidget(self)
        self.answers_widget = Lesson2AnswersWidget(self)

        self.question_generator = Lesson2QuestionGenerator(self)
        self.answers_generator = Lesson2AnswersGenerator(self)

        self.main_layout.addWidget(self.question_widget)
        self.main_layout.addWidget(self.answers_widget)
        self.main_layout.addWidget(self.indicator_label)

    def clear_current_question(self):
        """Clear the current question by resetting both question and answer widgets."""
        self.question_widget.clear()
        self.answers_widget.clear()

    def resize_lesson_widget(self):
        """Resize all the components (question and answers) based on window size."""
        self.question_widget.resize_lesson_2_question_widget()
        self.answers_widget.resize_lesson_2_answers_widget()
        super().resize_lesson_widget()
