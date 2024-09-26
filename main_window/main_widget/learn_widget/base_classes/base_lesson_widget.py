from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import (
    QTimer,
    Qt,
)

from main_window.main_widget.learn_widget.base_classes.results_widget import (
    ResultsWidget,
)

from .base_answers_widget import BaseAnswersWidget
from .base_question_generator import BaseQuestionGenerator
from .base_question_widget import BaseQuestionWidget
from ..lesson_widget_indicator_label import LessonWidgetIndicatorLabel

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class BaseLessonWidget(QWidget):
    """Base class for all lesson widgets, managing shared logic for questions and answers."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)
        self.learn_widget = learn_widget
        self.main_widget = learn_widget.main_widget

        # Main layout
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

        self.results_widget = ResultsWidget(self)
        self.indicator_label = LessonWidgetIndicatorLabel(self)

        # Timer for countdown mode
        self.quiz_timer = QTimer()
        self.quiz_timer.timeout.connect(self.update_quiz_timer)

        # Progress and result labels
        self.progress_label = self.create_label(alignment=Qt.AlignmentFlag.AlignCenter)
        self.result_label = self.create_label(alignment=Qt.AlignmentFlag.AlignCenter)

        # Start Over button
        self.start_over_button = QPushButton("Start Over")
        self.start_over_button.clicked.connect(self.prepare_quiz_ui)
        self.start_over_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Default attributes for quiz modes
        self.total_questions = 30
        self.current_question = 1
        self.quiz_time = 120
        self.mode = "fixed_question"


    def _setup_layout(self):
        """Setup common UI layout."""
        self.central_layout.addWidget(self.progress_label)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.question_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.answers_widget)
        self.central_layout.addStretch(1)
        self.central_layout.addWidget(self.indicator_label)
        self.central_layout.addStretch(1)

    def show_results(self):
        """Display the results after the quiz or countdown ends with animations."""
        self.clear_layout(self.central_layout)
        self.central_layout.addWidget(self.results_widget)

        # Set the result text dynamically
        self.results_widget.set_result_text(
            f"🎉 Well done!! 🎉\n\n"
            f"You successfully completed {self.current_question - 1} question"
            f"{'s' if self.current_question - 1 != 1 else ''}!"
        )

    def set_mode(self, mode: str) -> None:
        """Set the quiz mode (Fixed Questions or Countdown)."""
        self.mode = mode
        if self.mode == "fixed_question":
            self.start_fixed_question_mode()
        elif self.mode == "countdown":
            self.start_countdown_mode()

    def start_fixed_question_mode(self):
        """Start the Fixed Question Mode by setting up the UI."""
        self.current_question = 1
        self.update_progress_label()

        if self.quiz_timer.isActive():
            self.quiz_timer.stop()

        self.prepare_quiz_ui()

    def start_countdown_mode(self):
        """Start the Countdown Mode by setting up the UI."""
        self.clear_layout(self.central_layout)
        self.prepare_quiz_ui()
        self.start_quiz_timer()

    def start_quiz_timer(self):
        """Start the 2-minute quiz timer."""
        self.quiz_time = 120
        self.update_quiz_timer()
        self.quiz_timer.start(1000)

    def update_quiz_timer(self):
        """Update the quiz timer each second."""
        minutes, seconds = divmod(self.quiz_time, 60)
        self.progress_label.setText(f"Time Remaining: {minutes}:{seconds:02d}")

        if self.quiz_time > 0:
            self.quiz_time -= 1
        else:
            self.quiz_timer.stop()
            self.show_results()

    def update_progress_label(self):
        """Update progress display for Fixed Question Mode."""
        self.progress_label.setText(f"{self.current_question}/{self.total_questions}")

    def prepare_quiz_ui(self):
        """Prepare and switch to the quiz interface layout."""
        self.current_question = 1
        self.update_progress_label()
        self.clear_layout(self.central_layout)
        self._setup_layout()  # Rebuild the layout
        self.start_new_question()

    def check_answer(self, selected_answer, correct_answer):
        """Check the answer and show feedback."""
        if selected_answer == correct_answer:
            self.indicator_label.show_message("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.current_question += 1

            if self.mode == "fixed_question":
                self.update_progress_label()
                if self.current_question <= self.total_questions:
                    self.start_new_question()
                else:
                    self.show_results()
            elif self.mode == "countdown":
                self.start_new_question()
        else:
            self.indicator_label.show_message("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")
            self.answers_widget.disable_answer(selected_answer)

    def start_new_question(self):
        """Start a new question for the lesson."""
        self.clear_current_question()
        self.question_generator.generate_question()
        self.resize_lesson_widget()

    def add_back_button(self):
        """Add a back button to return to the lesson selection screen."""
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.learn_widget.show_lesson_selection_widget)
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_layout.addWidget(self.back_button)
        self.back_layout.addStretch(1)
        self.main_layout.addLayout(self.back_layout, 0)

    def create_label(self, alignment=None) -> QLabel:
        """Helper to create QLabel with optional alignment."""
        label = QLabel("")
        if alignment:
            label.setAlignment(alignment)
        return label

    def clear_layout(self, layout: QVBoxLayout):
        """Utility to clear a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if widget := item.widget():
                    widget.setParent(None)
                elif nested_layout := item.layout():
                    self.clear_layout(nested_layout)

    def resize_lesson_widget(self):
        """Resize UI elements dynamically."""
        self.question_widget._resize_question_widget()
        self.answers_widget.resize_answers_widget()
        self._resize_indicator_label()
        self._resize_back_button()
        self._resize_progress_label()
        self.results_widget.resize_results_widget()

    def _resize_start_over_button(self):
        start_over_button_font_size = self.main_widget.width() // 60
        self.start_over_button.setStyleSheet(
            f"font-size: {start_over_button_font_size}px;"
        )
        self.start_over_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )

    def _resize_result_label(self):
        result_label_font_size = self.main_widget.width() // 60
        font = self.result_label.font()
        font.setPointSize(result_label_font_size)
        self.result_label.setFont(font)

    def _resize_progress_label(self):
        progress_label_font_size = self.main_widget.width() // 75
        font = self.progress_label.font()
        font.setPointSize(progress_label_font_size)
        self.progress_label.setFont(font)

    def _resize_indicator_label(self):
        self.indicator_label.setFixedHeight(self.main_widget.height() // 20)
        indicator_label_font_size = self.main_widget.width() // 75
        font = self.indicator_label.font()
        font.setPointSize(indicator_label_font_size)
        self.indicator_label.setFont(font)

    def _resize_back_button(self):
        back_button_font_size = self.main_widget.width() // 60
        self.back_button.setFixedSize(
            self.main_widget.width() // 8, self.main_widget.height() // 12
        )
        self.back_button.setStyleSheet(f"font-size: {back_button_font_size}px;")

    def clear_current_question(self):
        """Clear the current question by resetting viewer and answer buttons."""
        self.question_widget.clear()
        self.answers_widget.clear()
