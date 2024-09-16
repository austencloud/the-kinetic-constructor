from typing import TYPE_CHECKING
from ..base_classes.base_lesson_widget import BaseLessonWidget
from .lesson_1_tracker_widget import Lesson1TrackerWidget
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .Lesson_1_question_widget import Lesson1QuestionWidget
from .lesson_1_question_generator import Lesson1QuestionGenerator
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget, handling pictograph to letter matching."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)

        self.question_widget = Lesson1QuestionWidget(self)
        self.answers_widget = Lesson1AnswersWidget(self)
        self.question_generator = Lesson1QuestionGenerator(self)
        self.tracker_widget = Lesson1TrackerWidget(self)

        self._setup_layout()
        self.main_layout.addWidget(self.tracker_widget)

    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.tracker_widget.increment_correct()
            self.indicator_label.show_message("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.start_new_question()
        else:
            self.tracker_widget.increment_incorrect()
            self.indicator_label.show_message("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")
            self.answers_widget.deactivate_answer(selected_answer)

    def resize_lesson_widget(self):
        super().resize_lesson_widget()
        self.tracker_widget.resize_tracker_widget()
