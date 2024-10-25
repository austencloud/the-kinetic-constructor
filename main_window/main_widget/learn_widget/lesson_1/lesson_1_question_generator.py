import random
from typing import TYPE_CHECKING
from Enums.letters import Letter
from main_window.main_widget.learn_widget.base_classes.base_question_generator import (
    BaseQuestionGenerator,
)


if TYPE_CHECKING:
    from .lesson_1_widget import Lesson1Widget


class Lesson1QuestionGenerator(BaseQuestionGenerator):
    """Generates questions for Lesson 1 (pictograph to letter matching)."""

    def __init__(self, lesson_1_widget: "Lesson1Widget") -> None:
        super().__init__(lesson_1_widget)
        self.lesson_1_widget = lesson_1_widget
        self.previous_correct_letter: Letter = None

    def generate_question(self):
        """Generate a question for Lesson 1."""
        correct_answer = self.generate_correct_answer()
        self.previous_correct_letter = correct_answer

        pictograph_dicts = self.filter_pictograph_dicts_by_grid_mode()

        correct_pictograph_dict = random.choice(pictograph_dicts[correct_answer])

        wrong_answers = self.generate_wrong_answers(correct_answer)
        self.lesson_1_widget.question_widget.load_pictograph(correct_pictograph_dict)

        letters = [correct_answer.value] + wrong_answers
        random.shuffle(letters)

        self.lesson_1_widget.answers_widget.display_answers(
            letters, correct_answer.value, self.lesson_1_widget.check_answer
        )

    def filter_pictograph_dicts_by_grid_mode(self) -> dict[Letter, list[dict]]:
        """Filter pictograph dicts by grid mode."""
        valid_dicts: dict[Letter, list[dict]] = {}
        grid_mode = self.main_widget.settings_manager.global_settings.get_grid_mode()
        for letter in self.main_widget.pictograph_dicts:
            valid_dicts.setdefault(letter, [])
            for pictograph_dict in self.main_widget.pictograph_dicts[letter]:
                if (
                    self.main_widget.grid_mode_checker.get_grid_mode(pictograph_dict)
                    == grid_mode
                ):
                    valid_dicts[letter].append(pictograph_dict)
        return valid_dicts

    def generate_correct_answer(self) -> Letter:
        """Generate a new correct letter that is different from the previous one."""
        letters = list(self.main_widget.pictograph_dicts.keys())
        if self.previous_correct_letter:
            letters.remove(self.previous_correct_letter)
        return random.choice(letters)

    def generate_wrong_answers(self, correct_answer) -> list[str]:
        """Generate three random wrong letter answers."""
        wrong_answers = random.sample(
            [
                letter.value
                for letter in self.main_widget.pictograph_dicts
                if letter != correct_answer
            ],
            3,
        )
        return wrong_answers
