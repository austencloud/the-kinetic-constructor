from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_widget.base_classes.base_question_widget import (
    BaseQuestionWidget,
)

if TYPE_CHECKING:
    from .lesson_2_widget import Lesson2Widget


class Lesson2QuestionWidget(BaseQuestionWidget):
    """Widget responsible for displaying the question in Lesson 2."""

    def __init__(self, lesson_2_widget: "Lesson2Widget") -> None:
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget
        self.main_widget = lesson_2_widget.main_widget
        self._setup_labels()
        self._setup_layout()

    def _setup_labels(self) -> None:
        self.question_label = QLabel("Choose the pictograph for:")
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.letter_label = QLabel()
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.question_label)
        self.layout.addWidget(self.letter_label)

    def _update_letter_label(self, letter: str) -> None:
        """Display the question prompt and the letter to be matched."""
        self.letter_label.setText(letter)

    def clear(self) -> None:
        """Clear the question display."""
        self.letter_label.clear()

    def resize_question_widget(self) -> None:
        """Resize the question labels based on window size."""
        self._resize_question_label()
        self._resize_letter_label()

    def _resize_letter_label(self):
        letter_label_font_size = self.main_widget.width() // 40
        letter_label_font = self.letter_label.font()
        letter_label_font.setFamily("Georgia")
        letter_label_font.setPointSize(letter_label_font_size)
        self.letter_label.setFont(letter_label_font)

    def _resize_question_label(self):
        question_label_font_size = self.main_widget.width() // 50
        question_label_font = self.question_label.font()
        question_label_font.setFamily("Monotype Corsiva")
        question_label_font.setPointSize(question_label_font_size)
        self.question_label.setFont(question_label_font)
