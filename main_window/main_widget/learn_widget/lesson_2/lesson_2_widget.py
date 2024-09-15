import random
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from main_window.main_widget.learn_widget.base_lesson_widget import BaseLessonWidget
from .lesson_2_answers_widget import Lesson2AnswersWidget
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget, handling letter to pictograph matching."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)

        # Add the letter label (which was missing in the refactored version)
        self.letter_label = QLabel()
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.insertWidget(
            3, self.letter_label
        )  # Add it below the question label

        # Add the pictograph buttons widget
        self.lesson_2_answers_widget = Lesson2AnswersWidget(learn_widget)
        self.main_layout.addWidget(self.lesson_2_answers_widget)
        self.main_layout.addWidget(self.indicator_label)
        self.main_layout.addStretch(3)

    def generate_question(self):
        """Show a letter and let the user guess the corresponding pictograph."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        # Set the question label text
        self.question_label.setText(f"Choose the pictograph for:")
        self.letter_label.setText(correct_letter.value)

        # Generate wrong pictographs
        wrong_pictographs = self.generate_random_wrong_pictographs(correct_letter)
        pictographs = [correct_pictograph_dict] + wrong_pictographs
        random.shuffle(pictographs)

        # Display the pictograph buttons
        self.lesson_2_answers_widget.create_pictograph_buttons(
            pictographs, correct_pictograph_dict, self.check_answer
        )

    def generate_random_wrong_pictographs(self, correct_letter) -> list[dict]:
        """Generate three random wrong pictographs, ensuring no repeats."""
        # Exclude previously used pictographs and the correct letter's pictographs
        available_letters = [
            letter for letter in self.main_widget.letters if letter != correct_letter
        ]

        wrong_pictographs = []
        while len(wrong_pictographs) < 3:
            letter = random.choice(available_letters)
            pictograph_dict = random.choice(self.main_widget.letters[letter])

            # Ensure the new pictograph wasn't used in the previous or current question
            pictograph_key = (
                self.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            if pictograph_key not in self.previous_pictographs:
                wrong_pictographs.append(pictograph_dict)
                self.previous_pictographs.add(pictograph_key)

        return wrong_pictographs

    def clear_current_question(self):
        """Clear the current question by resetting answer buttons."""
        self.lesson_2_answers_widget.clear()

    def resize_lesson_widget(self):
        """Resize the pictograph buttons and other elements based on window size."""
        self.lesson_2_answers_widget.resize_lesson_2_answers_widget()
        self._resize_question_label()
        self._resize_back_button()
        self._resize_indicator_label()
        self._resize_letter_label()

    def _resize_letter_label(self):
        letter_label_font_size = self.main_widget.width() // 40
        font = self.letter_label.font()
        font.setFamily("Arial")
        font.setPointSize(letter_label_font_size)
        self.letter_label.setFont(font)
