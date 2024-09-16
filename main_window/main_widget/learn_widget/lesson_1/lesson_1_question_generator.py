import random
from typing import TYPE_CHECKING
from Enums.letters import Letter
from main_window.main_widget.learn_widget.base_question_generator import (
    BaseQuestionGenerator,
)

if TYPE_CHECKING:
    from .lesson_1_widget import Lesson1Widget


class Lesson1QuestionGenerator(BaseQuestionGenerator):
    """Generates questions for Lesson 1 (pictograph to letter matching)."""

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.previous_correct_letter: Letter = None

    def generate_question(self):
        """Generate a question for Lesson 1."""
        correct_letter = self.generate_correct_answer()
        self.previous_correct_letter = correct_letter

        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        wrong_answers = self.generate_wrong_answers(correct_letter)
        self.lesson_1_widget.question_widget.load_pictograph(correct_pictograph_dict)

        letters = [correct_letter.value] + wrong_answers
        random.shuffle(letters)

        self.lesson_1_widget.answers_widget.display_answers(
            letters, correct_letter.value, self.lesson_1_widget.check_answer
        )

    def generate_correct_answer(self) -> Letter:
        """Generate a new correct letter that is different from the previous one."""
        letters = list(self.main_widget.letters.keys())
        if self.previous_correct_letter:
            letters.remove(self.previous_correct_letter)
        return random.choice(letters)

    def generate_wrong_answers(self, correct_letter) -> list[str]:
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
