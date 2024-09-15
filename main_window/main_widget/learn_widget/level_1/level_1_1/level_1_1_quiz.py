import random
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .level_1_1_quiz_pictograph_buttons_widget import (
    Level_1_1_QuizPictographButtonsWidget,
)

if TYPE_CHECKING:
    from ...learn_widget import LearnWidget


class Level_1_1_Quiz(QWidget):
    """Quiz class for showing a letter and letting the user choose the correct pictograph."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        self.pictograph_buttons_widget = Level_1_1_QuizPictographButtonsWidget(
            learn_widget
        )

        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Variable to store the keys of the previously shown pictographs
        self.previous_pictographs = set()

        self.add_back_button()
        self.main_layout.addStretch(1)
        
        self.question_label = QLabel()
        self.letter_label = QLabel()
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.question_label)
        self.main_layout.addWidget(self.letter_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.pictograph_buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.indicator_label = QLabel("")
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.indicator_label)

        self.main_layout.addStretch(3)

    def add_back_button(self):
        """Add a back button to go back to the Level1QuizSelector."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_level_1_quiz_selector)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)

        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button)
        back_layout.addStretch(1)

        self.main_layout.insertLayout(0, back_layout)

    def start_new_question(self):
        """Start a new question for the user."""
        self.clear_current_question()
        self.generate_question()  # Letter -> Pictograph
        self.resize_level_1_1_quiz()

    def generate_question(self):
        """Show a letter and let the user guess the corresponding pictograph."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        # Set the question label text
        self.question_label.setText(f"Choose the pictograph for:")
        self.letter_label.setText(correct_letter.value)

        # Generate three new wrong pictographs that are not part of the previous ones
        wrong_pictographs = self.generate_random_wrong_pictographs(correct_letter)

        # Include the correct pictograph and shuffle the order
        pictographs = [correct_pictograph_dict] + wrong_pictographs
        random.shuffle(pictographs)

        # Store the keys of the new pictographs to avoid repeating in the next question
        self.previous_pictographs = set(
            self.main_widget.pictograph_key_generator.generate_pictograph_key(pictograph)
            for pictograph in pictographs
        )

        # Display the pictograph buttons
        self.pictograph_buttons_widget.create_pictograph_buttons(
            pictographs, correct_pictograph_dict, self.check_answer
        )

    def check_answer(self, selected_pictograph, correct_pictograph):
        """Check if the selected pictograph is correct."""
        if selected_pictograph == correct_pictograph:
            self.indicator_label.setText("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.start_new_question()
        else:
            self.indicator_label.setText("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")

    def clear_current_question(self):
        """Clear the current question before generating a new one."""
        self.pictograph_buttons_widget.clear()

    def generate_random_wrong_pictographs(self, correct_letter) -> list[dict]:
        """Generate three random wrong pictographs, avoiding repeats."""
        # Exclude previously used pictographs and the correct letter's pictographs
        available_letters = [
            letter
            for letter in self.main_widget.letters
            if letter != correct_letter
        ]

        # Get pictographs that haven't been used in the previous question
        wrong_pictographs = []
        while len(wrong_pictographs) < 3:
            letter = random.choice(available_letters)
            pictograph = random.choice(self.main_widget.letters[letter])

            # Ensure the new pictograph wasn't used in the previous question
            pictograph_key = self.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph
            )
            if pictograph_key not in self.previous_pictographs:
                wrong_pictographs.append(pictograph)

        return wrong_pictographs

    def resize_level_1_1_quiz(self):
        """Resize the pictograph buttons and other elements based on window size."""
        self.pictograph_buttons_widget.resize_level_1_1_pictograph_buttons_widget()
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

    def _resize_question_label(self):
        question_label_font_size = self.learn_widget.width() // 50
        font = self.question_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(question_label_font_size)
        self.question_label.setFont(font)

    def _resize_back_button(self):
        back_button_font_size = self.main_widget.width() // 60
        self.back_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )
        self.back_button.setStyleSheet(f"font-size: {back_button_font_size}px;")

    def _resize_indicator_label(self):
        self.indicator_label.setFixedHeight(self.main_widget.height() // 20)
        indicator_label_font_size = self.main_widget.width() // 75
        font = self.indicator_label.font()
        font.setPointSize(indicator_label_font_size)
        self.indicator_label.setFont(font)
