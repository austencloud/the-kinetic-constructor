import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import (
        Lesson2Widget,
    )


class Lesson2AnswersGenerator:
    """Generates the correct and wrong answers for Lesson 2."""

    def __init__(self, lesson_2_widget: "Lesson2Widget"):
        self.lesson_2_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget

    def generate_answers(self, correct_pictograph_dict: dict) -> list[dict]:
        """Generates a list of pictographs, including the correct one and random wrong ones."""
        wrong_pictographs = self.generate_random_wrong_pictographs(
            correct_pictograph_dict["letter"]
        )
        return [correct_pictograph_dict] + wrong_pictographs

    def generate_random_wrong_pictographs(self, correct_letter: str) -> list[dict]:
        """Generate three random wrong pictographs, ensuring each has a different letter."""
        available_letters = [
            letter for letter in self.main_widget.letters if letter != correct_letter
        ]

        wrong_pictographs = []
        used_letters = {correct_letter}  # Ensure we don't reuse the correct letter

        while len(wrong_pictographs) < 3:
            letter = random.choice(available_letters)

            if letter in used_letters:
                continue  # Skip if we've already used this letter

            pictograph_dict = random.choice(self.main_widget.letters[letter])

            pictograph_key = (
                self.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            if (
                pictograph_key
                not in self.lesson_2_widget.question_generator.previous_pictographs
            ):
                wrong_pictographs.append(pictograph_dict)
                self.lesson_2_widget.question_generator.previous_pictographs.add(
                    pictograph_key
                )
                used_letters.add(letter)

        return wrong_pictographs
