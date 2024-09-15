import random
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class BaseLessonWidget(QWidget):
    """Base class for all lesson widgets, managing shared logic for questions and answers."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        # Main layout
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label = QLabel("")
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add back button
        self.add_back_button()

        # Add other shared components
        # self.main_layout.addStretch(1)

    def add_back_button(self):
        """Add a back button to return to the lesson selection screen."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_lesson_selection_widget)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        back_layout = QHBoxLayout()
        back_layout.addWidget(self.back_button)
        back_layout.addStretch(1)
        self.main_layout.insertLayout(0, back_layout)

    def start_new_question(self):
        """Start a new question for the lesson."""
        self.clear_current_question()
        self.question_generator.generate_question()
        self.resize_lesson_widget()

    def generate_question(self):
        """Generate a new question for the lesson (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")

    def clear_current_question(self):
        """Clear the current question (to be implemented by subclasses)."""
        raise NotImplementedError("Subclasses must implement this method.")

    def check_answer(self, selected_answer, correct_answer):
        """Check if the selected answer is correct."""
        if selected_answer == correct_answer:
            self.indicator_label.setText("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.start_new_question()
        else:
            self.indicator_label.setText("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")

    def resize_lesson_widget(self):
        """Resize the components based on window size."""
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
