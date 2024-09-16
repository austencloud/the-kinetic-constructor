from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from .base_answers_widget import BaseAnswersWidget
from .base_question_generator import BaseQuestionGenerator
from .base_question_widget import BaseQuestionWidget
from ..lesson_widget_indicator_label import LessonWidgetIndicatorLabel

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class BaseLessonWidget(QWidget):
    """Base class for all lesson widgets, managing shared logic for questions and answers."""

    def __init__(self, learn_widget: "LearnWidget"):
        self.learn_widget = learn_widget
        super().__init__(learn_widget)
        self.main_widget = learn_widget.main_widget
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.central_layout: QVBoxLayout = QVBoxLayout()
        self.back_layout: QHBoxLayout = QHBoxLayout()

        self.setLayout(self.main_layout)

        # Add back button and central area to the main layout
        self.add_back_button()
        self.main_layout.addLayout(self.central_layout)

        self.question_generator: BaseQuestionGenerator = None
        self.question_widget: BaseQuestionWidget = None
        self.answers_widget: BaseAnswersWidget = None

        self._setup_indicator_label()
        self._setup_layout()

    def _setup_layout(self):
        self.central_layout.addWidget(self.question_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.answers_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.indicator_label)
        self.central_layout.addStretch(1)

    def _setup_indicator_label(self):
        self.indicator_label = LessonWidgetIndicatorLabel(self)

    def add_back_button(self):
        """Add a back button to return to the lesson selection screen."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_lesson_selection_widget)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_layout.addWidget(self.back_button)
        self.back_layout.addStretch(1)
        self.main_layout.addLayout(self.back_layout, 0)

    def start_new_question(self):
        """Start a new question for the lesson."""
        self.clear_current_question()
        self.question_generator.generate_question()
        self.resize_lesson_widget()

    def resize_lesson_widget(self):
        self.question_widget._resize_question_widget()
        self.answers_widget.resize_answers_widget()
        self._resize_indicator_label()
        self._resize_back_button()

    def check_answer(self, selected_answer, correct_answer):
        if selected_answer == correct_answer:
            self.indicator_label.show_message("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.start_new_question()
        else:
            self.indicator_label.show_message("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")

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

    def clear_current_question(self):
        """Clear the current question by resetting viewer and answer buttons."""
        self.question_widget.clear()
        self.answers_widget.clear()
