import random
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import (
        Lesson1Widget,
    )


class Lesson1QuestionGenerator:
    """Generates questions for Lesson 1 (pictograph to letter matching)."""

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        self.lesson_1_widget = lesson_1_widget
        self.main_widget = lesson_1_widget.main_widget

    def generate_question(self):
        """Generate a question for Lesson 1."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                correct_pictograph_dict
            )
        )
        wrong_answers = self.generate_random_wrong_answers(correct_letter)

        # Load the pictograph
        self.lesson_1_widget.pictograph_viewer.load_pictograph(
            pictograph_key, correct_pictograph_dict
        )

        # Set the question text and create answer buttons
        self.lesson_1_widget.question_label.setText("Choose the matching letter:")
        letters = [correct_letter.value] + wrong_answers
        random.shuffle(letters)

        self.lesson_1_widget.answers_widget.create_answer_buttons(
            letters, correct_letter.value, self.lesson_1_widget.check_answer
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
