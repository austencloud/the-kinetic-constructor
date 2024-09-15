from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget


class LessonSelector(QWidget):
    """Widget for selecting lessons in the learning module."""

    def __init__(self, learn_widget: "LearnWidget") -> None:
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        # Layout setup
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Title label
        self.title_label = QLabel("Select a Lesson:")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add elements to layout
        self.layout.addStretch(2)
        self.layout.addWidget(self.title_label)
        self.layout.addStretch(2)

        # Add buttons for each lesson
        self.add_lesson_button(
            "Lesson 1 - Pictograph to Letter",
            self.learn_widget.start_lesson_1,
        )
        self.add_lesson_button(
            "Lesson 2 - Letter to Pictograph", self.learn_widget.start_lesson_2
        )
        self.layout.addStretch(2)

    def add_lesson_button(self, text: str, callback) -> None:
        """Create and add a button for lesson selection."""
        button = QPushButton(text)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        self.layout.addStretch(1)

    def resize_lesson_selector(self) -> None:
        """Resize title and buttons based on window size."""
        self._resize_title_label()
        self._resize_buttons()


    def _resize_title_label(self):
        title_font_size = self.main_widget.width() // 40
        font = self.title_label.font()
        font.setFamily("Monotype Corsiva")  # Set font family to Monotype Corsiva
        font.setPointSize(title_font_size)
        self.title_label.setFont(font)

    def _resize_buttons(self):
        button_font_size = self.main_widget.width() // 60
        for button in self.findChildren(QPushButton):
            button.setFixedSize(
                self.main_widget.width() // 4, self.main_widget.height() // 8
            )
            button.setStyleSheet(f"font-size: {button_font_size}px;")
