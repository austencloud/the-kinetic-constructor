from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from main_window.main_widget.learn_tab.base_classes.base_lesson_widget.lesson_widget_go_back_button import (
    LessonWidgetGoBackButton,
)
from ..base_answers_widget import BaseAnswersWidget
from .lesson_layout_manager import LessonLayoutManager
from .quiz_timer_manager import QuizTimerManager
from ..base_question_generator import BaseQuestionGenerator
from ..base_question_widget import BaseQuestionWidget
from ...lesson_widget_indicator_label import LessonWidgetIndicatorLabel
from .results_widget import ResultsWidget

if TYPE_CHECKING:
    from ...learn_tab import LearnTab


class BaseLessonWidget(QWidget):
    """Base class for all lesson widgets, managing shared logic for questions and answers."""

    def __init__(self, learn_tab: "LearnTab"):
        super().__init__(learn_tab)
        self.learn_tab = learn_tab
        self.main_widget = learn_tab.main_widget

        # Managers and widgets
        self.layout_manager = LessonLayoutManager(self)
        self.timer_manager = QuizTimerManager(self)
        self.results_widget = ResultsWidget(self)
        self.indicator_label = LessonWidgetIndicatorLabel(self)
        self.fade_manager = self.main_widget.fade_manager

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
        self.incorrect_guesses = 0

    def _setup_layout(self):
        """Setup common UI layout."""
        self.layout_manager.setup_layout()

    def show_results(self):
        """Display the results after the quiz or countdown ends."""
        self.results_widget.show_results(self.incorrect_guesses)

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

        self.timer_manager.stop_timer()
        self.prepare_quiz_ui()

    def start_countdown_mode(self):
        """Start the Countdown Mode by setting up the UI."""
        self.clear_layout(self.central_layout)
        self.prepare_quiz_ui()
        self.timer_manager.start_timer(120)  # 2 minutes countdown

    def start_quiz_timer(self):
        """Start the quiz timer."""
        self.timer_manager.start_timer(120)

    def update_progress_label(self):
        """Update progress display for Fixed Question Mode."""
        self.progress_label.setText(f"{self.current_question}/{self.total_questions}")

    def prepare_quiz_ui(self):
        """Prepare and switch to the quiz interface layout."""
        self.current_question = 1
        self.incorrect_guesses = 0
        self.update_progress_label()
        self.clear_layout(self.central_layout)
        self.layout_manager.setup_layout()
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
                    self.results_widget.show_results(self.incorrect_guesses)
            elif self.mode == "countdown":
                self.start_new_question()
        else:
            self.indicator_label.show_message("Wrong! Try again.")
            self.indicator_label.setStyleSheet("color: red;")
            self.answers_widget.disable_answers(selected_answer)
            self.incorrect_guesses += 1

    def start_new_question(self):
        widgets_to_fade = [
            self.question_widget,
            self.answers_widget,
        ]
        self.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=self._generate_new_question,
        )

    def _generate_new_question(self):
        self.clear_current_question()
        self.question_generator.generate_question()

    def add_back_button(self):
        """Add a back button to return to the lesson selection screen."""
        self.go_back_button = LessonWidgetGoBackButton(self)
        self.back_layout.addWidget(self.go_back_button)
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

    def clear_current_question(self):
        """Clear the current question by resetting viewer and answer buttons."""
        self.question_widget.clear()
        self.answers_widget.clear()

    def resizeEvent(self, event):
        """Resize UI elements dynamically."""
        self.layout_manager.resize_widgets()
