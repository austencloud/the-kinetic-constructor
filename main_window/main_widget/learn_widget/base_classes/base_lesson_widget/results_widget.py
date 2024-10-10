from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.base_lesson_widget import (
        BaseLessonWidget,
    )

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class ResultsWidget(QWidget):
    """Widget containing the result label and the 'Start Over' button."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        super().__init__(lesson_widget)
        self.lesson_widget = lesson_widget
        self.main_widget = lesson_widget.main_widget

        # Create result label and start over button
        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("color: blue; font-weight: bold;")

        self.start_over_button = QPushButton("Start Over", self)
        self.start_over_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_over_button.clicked.connect(self.lesson_widget.prepare_quiz_ui)

        # Layout setup
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(3)

        # Add the result label and button, centering them
        self.layout.addWidget(self.result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.start_over_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout.addStretch(3)

        self.setLayout(self.layout)

    def set_result_text(self, text: str):
        """Set the result text for the result label."""
        self.result_label.setText(text)
        self.adjustSize()

    def resize_results_widget(self):
        """Resize the result label and start-over button to fit the content."""
        self._resize_result_label()
        self._resize_start_over_button()

    def _resize_start_over_button(self):
        start_over_button_font_size = self.main_widget.width() // 60
        self.start_over_button.setStyleSheet(
            f"font-size: {start_over_button_font_size}px;"
        )
        self.start_over_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )

    def _resize_result_label(self):
        result_label_font_size = self.main_widget.width() // 75
        font = self.result_label.font()
        font.setPointSize(result_label_font_size)
        self.result_label.setFont(font)
        self.result_label.adjustSize()

    def show_results(self, incorrect_guesses):
        """Display the results after the quiz or countdown ends."""
        self.lesson_widget.clear_layout(self.lesson_widget.central_layout)
        self.lesson_widget.central_layout.addWidget(self)

        self.set_result_text(
            f"🎉 Well done!! 🎉\n\n"
            + f"You successfully completed {self.lesson_widget.current_question - 1} question"
            + f"{'s' if self.lesson_widget.current_question - 1 != 1 else ''}"
            + (
                f"!\nwithout making any mistakes! Great job!"
                if incorrect_guesses == 0
                else f" but you made {incorrect_guesses} mistakes. Keep on practicing!"
            )
        )
