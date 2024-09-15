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
from .level_1_0_quiz_answer_buttons_widget import Level_1_0_QuizAnswerButtonsWidget
from .level_1_0_quiz_pictograph_viewer import Level_1_0_QuizPictographViewer

if TYPE_CHECKING:
    from ...learn_widget import LearnWidget


class Level_1_0_Quiz(QWidget):
    """Main quiz class, coordinating pictograph, questions, and answers."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        self.pictograph_viewer = Level_1_0_QuizPictographViewer(learn_widget)
        self.answer_buttons_widget = Level_1_0_QuizAnswerButtonsWidget(learn_widget)

        # Main layout for the quiz widget
        self.main_layout: QVBoxLayout = QVBoxLayout()
        # self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

        # Add back button at the top left
        self.add_back_button()

        self.main_layout.addStretch(1)
        # Question label
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.question_label)

        # Add the pictograph viewer and answer buttons to the layout
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.pictograph_viewer, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(
            self.answer_buttons_widget, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Add the indicator label for correct/wrong answer
        self.indicator_label = QLabel("")
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label.show()
        # self.indicator_label.hide()  # Initially hidden
        self.main_layout.addWidget(self.indicator_label)

        self.main_layout.addStretch(3)

    def add_back_button(self):
        """Add a back button to go back to Level1QuizSelector."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_level_1_quiz_selector)
        # pointing hand cursor
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        # Create a horizontal layout for the back button
        back_layout = QHBoxLayout()

        # Add a stretch AFTER the button to ensure it stays aligned left
        back_layout.addWidget(self.back_button)
        back_layout.addStretch(1)  # Add stretch to push other elements to the right

        # Add back_layout to the main layout at the top
        self.main_layout.insertLayout(0, back_layout)

    def start_new_question(self):
        self.clear_current_question()
        self.generate_question()  # Pictograph -> Letter
        self.resize_level_1_0_quiz()

    def generate_question(self):
        """Show a pictograph and let the user guess the corresponding letter."""
        correct_letter = random.choice(list(self.main_widget.letters.keys()))
        correct_pictograph_dict = random.choice(
            self.main_widget.letters[correct_letter]
        )

        # Generate the pictograph
        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                correct_pictograph_dict
            )
        )
        self.pictograph_viewer.load_pictograph(pictograph_key, correct_pictograph_dict)

        # Set the question label text
        self.question_label.setText("Choose the matching letter:")

        # Generate answer buttons (one correct and three random wrong ones)
        correct_answer = correct_letter.value
        wrong_answers = self.generate_random_wrong_answers(correct_letter)

        letters = [correct_answer] + wrong_answers
        random.shuffle(letters)  # Shuffle the options

        # Create answer buttons
        self.answer_buttons_widget.create_answer_buttons(
            letters, correct_answer, self.check_answer
        )

    def check_answer(self, selected_answer, correct_answer):
        """Check if the selected letter is correct."""
        if selected_answer == correct_answer:
            self.indicator_label.setText("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.start_new_question()
        else:
            self.indicator_label.setText("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")

    def clear_current_question(self):
        """Clear the current question before generating a new one."""
        self.pictograph_viewer.clear()
        self.answer_buttons_widget.clear()

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

    def resize_level_1_0_quiz(self):
        """Resize the pictograph and answer buttons based on the window size."""
        self.pictograph_viewer.resize_level_1_0_quiz_pictograph_viewer()
        self.answer_buttons_widget.resize_level_1_0_answer_buttons_widget()
        self._resize_question_label()
        self._resize_back_button()
        self._resize_indicator_label()

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
