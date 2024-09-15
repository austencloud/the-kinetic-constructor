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
from .Lesson_1_pictograph_viewer import Lesson1PictographViewer

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


from .lesson_1_answers_widget import Lesson1AnswersWidget


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget, handling pictograph to letter matching."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)

        self.pictograph_viewer = Lesson1PictographViewer(learn_widget)
        self.answer_buttons_widget = Lesson1AnswersWidget(learn_widget)

        # Add specific components for lesson 1
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.pictograph_viewer)
        self.main_layout.addWidget(self.answer_buttons_widget)
        self.main_layout.addWidget(self.indicator_label)
        self.main_layout.addStretch(3)

    def generate_question(self):
        """Show a pictograph and let the user guess the corresponding letter."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                correct_pictograph_dict
            )
        )
        self.pictograph_viewer.load_pictograph(pictograph_key, correct_pictograph_dict)

        self.question_label.setText("Choose the matching letter:")

        correct_answer = correct_letter.value
        wrong_answers = self.generate_random_wrong_answers(correct_letter)

        letters = [correct_answer] + wrong_answers
        random.shuffle(letters)

        self.answer_buttons_widget.create_answer_buttons(
            letters, correct_answer, self.check_answer
        )

    def generate_random_wrong_answers(self, correct_letter) -> list[str]:
        """Generate three random wrong letter answers."""
        wrong_answers = random.sample(
            [
                letter.value
                for letter in self.main_widget.letters
                if letter != correct_letter
            ],
            3,
        )
        return wrong_answers

    def clear_current_question(self):
        """Clear the current question by resetting viewer and answer buttons."""
        self.pictograph_viewer.clear()
        self.answer_buttons_widget.clear()

    def resize_lesson_widget(self):
        self.pictograph_viewer.resize_lesson_1_pictograph_viewer()
        self.answer_buttons_widget.resize_lesson_1_answers_widget()
        super().resize_lesson_widget()
