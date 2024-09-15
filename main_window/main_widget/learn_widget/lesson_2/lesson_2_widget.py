from ..base_lesson_widget import BaseLessonWidget
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

    def _setup_layout(self) -> None:
        self.layout.addStretch(1)
        self.layout.addWidget(self.question_widget)
        self.layout.addWidget(self.answers_widget)
        self.layout.addWidget(self.indicator_label)
        self.layout.addStretch(1)

    def clear_current_question(self) -> None:
        """Clear the current question by resetting both question and answer widgets."""
        self.question_widget.clear()
        self.answers_widget.clear()

    def resize_lesson_widget(self) -> None:
        """Resize all the components (question and answers) based on window size."""
        self.question_widget.resize_lesson_2_question_widget()
        self.answers_widget.resize_lesson_2_answers_widget()
        super().resize_lesson_widget()
