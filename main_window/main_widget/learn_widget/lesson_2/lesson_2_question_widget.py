from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class Lesson2QuestionWidget(QWidget):
    """Widget responsible for displaying the question in Lesson 2."""

    def __init__(self, lesson_2_widget):
        super().__init__(lesson_2_widget)
        self.lesson_2_widget = lesson_2_widget

        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        # Question label (prompt)
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.question_label)

        # Letter label (letter to be matched)
        self.letter_label = QLabel()
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.letter_label)

    def display_question(self, question_text: str, letter: str):
        """Display the question prompt and the letter to be matched."""
        self.question_label.setText(question_text)
        self.letter_label.setText(letter)

    def clear(self):
        """Clear the question display."""
        self.question_label.clear()
        self.letter_label.clear()

    def resize_lesson_2_question_widget(self):
        """Resize the question labels based on window size."""
        font_size = self.lesson_2_widget.main_widget.width() // 50
        self.question_label.setStyleSheet(f"font-size: {font_size}px;")
        self.letter_label.setStyleSheet(f"font-size: {font_size}px;")
