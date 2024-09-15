from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class Level_1_0_QuizAnswerButtonsWidget(QWidget):
    """Widget to manage answer buttons layout and actions."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.buttons: list[QPushButton] = []

    def create_answer_buttons(self, letters, correct_answer, check_answer_callback):
        """Create the answer buttons and attach click events."""
        for letter in letters:
            button = QPushButton(letter)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda _, opt=letter: check_answer_callback(opt, correct_answer)
            )
            self.layout.addWidget(button)
            self.buttons.append(button)

    def clear(self):
        """Clear all buttons."""
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()

    def resize_level_1_0_answer_buttons_widget(self):
        for button in self.buttons:
            button.setFixedSize(
                self.main_widget.width() // 10, self.main_widget.height() // 10
            )
            font_size = self.main_widget.width() // 40
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setStyleSheet(f"font-size: {font_size}px;")
