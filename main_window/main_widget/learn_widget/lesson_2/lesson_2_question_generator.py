import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .lesson_2_widget import Lesson2Widget


class Lesson2QuestionGenerator:
    """Generates questions for Lesson 2 (letter to pictograph matching)."""

    def __init__(self, lesson_2_widget: "Lesson2Widget") -> None:
        self.lesson_2_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget
        self.previous_pictographs = set()

    def generate_question(self):
        """Generate the question and pass it to the QuestionWidget."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        # Display the generated question in the question widget
        self.lesson_2_widget.question_widget.display_question(
            "Choose the pictograph for:", correct_letter.value
        )

        pictographs = self.lesson_2_widget.answers_generator.generate_answers(
            correct_pictograph_dict
        )
        random.shuffle(pictographs)

        # Display the answers in the AnswersWidget
        self.lesson_2_widget.answers_widget.display_answers(
            pictographs, correct_pictograph_dict, self.lesson_2_widget.check_answer
        )
