from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from ..base_classes.base_lesson_widget import BaseLessonWidget
from .lesson_1_answers_widget import Lesson1AnswersWidget
from .lesson_1_question_widget import Lesson1QuestionWidget
from .lesson_1_question_generator import Lesson1QuestionGenerator

if TYPE_CHECKING:
    from ..learn_widget import LearnWidget


class Lesson1Widget(BaseLessonWidget):
    """Lesson 1 widget for handling mode selection and quiz logic."""

    def __init__(self, learn_widget: "LearnWidget"):
        super().__init__(learn_widget)

        # Override question and answer widgets in the base class
        self.question_widget = Lesson1QuestionWidget(self)
        self.answers_widget = Lesson1AnswersWidget(self)
        self.question_generator = Lesson1QuestionGenerator(self)

        # Countdown and quiz timers
        self.progress_label = QLabel()  # For question count or countdown timer
        self.countdown_timer = QTimer()  # Separate timer for 3-2-1 countdown
        self.quiz_timer = QTimer()  # Separate timer for quiz
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Timer connection for countdown and quiz
        self.quiz_timer.timeout.connect(self.update_quiz_timer)

        self.countdown_time = 3
        self.quiz_time = 120
        self.total_questions = 1
        self.current_question = 1

        # Set up mode selection first
        self.setup_mode_selection()

    def setup_mode_selection(self):
        """Setup the initial mode selection layout with buttons for the modes."""
        self.clear_layout(self.central_layout)

        self.mode_selection_layout = QHBoxLayout()
        self.mode_selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the buttons for mode selection
        self.fixed_question_button = QPushButton("Start Fixed Question")
        self.countdown_button = QPushButton("Start Countdown")

        self.fixed_question_button.clicked.connect(self.start_fixed_question_mode)
        self.countdown_button.clicked.connect(self.start_countdown_mode)

        # set the cursors to pointing hand
        self.fixed_question_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.countdown_button.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add mode buttons to layout
        self.mode_selection_layout.addWidget(self.fixed_question_button)
        self.mode_selection_layout.addWidget(self.countdown_button)

        # Add the mode selection layout to the central area
        self.central_layout.addLayout(self.mode_selection_layout)
        self.resize_lesson_widget()

    def start_fixed_question_mode(self):
        """Start the Fixed Question Mode by setting up the UI."""
        self.mode = "fixed_question"

        self.current_question = 1
        self.update_fixed_question_progress_label()

        self.clear_layout(self.central_layout)

        if self.countdown_timer.isActive():
            self.countdown_timer.stop()
        if self.quiz_timer.isActive():
            self.quiz_timer.stop()

        self.prepare_quiz_ui()
        self.update_fixed_question_progress_label()

    def start_countdown_mode(self):
        """Start the Countdown Mode with a countdown and show a loading message first."""
        self.mode = "countdown"
        self.clear_layout(self.central_layout)

        self.quiz_layout = QVBoxLayout()
        self.central_layout.addLayout(self.quiz_layout)

        self.clear_layout(self.central_layout)
        self.prepare_quiz_ui()
        self.start_quiz_timer()  # Start the quiz timer after the countdown

    def start_quiz_timer(self):
        """Start the 2:00 quiz timer and update the progress label."""
        self.quiz_time = 120  # 2 minutes for the quiz
        self.update_quiz_timer()  # Show the initial time
        self.quiz_timer.start(1000)  # Update every second

    def update_quiz_timer(self):
        """Update the quiz timer every second."""
        minutes, seconds = divmod(self.quiz_time, 60)
        self.progress_label.setText(f"Time Remaining: {minutes}:{seconds:02d}")

        if self.quiz_time > 0:
            self.quiz_time -= 1
        else:
            self.quiz_timer.stop()
            self.show_results()

    def prepare_quiz_ui(self):
        """Prepare and switch to the quiz/challenge interface layout."""
        self.clear_layout(self.central_layout)
        self.quiz_layout = QVBoxLayout()

        # Add the progress or countdown above the question widget
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.quiz_layout.addStretch(1)
        self.quiz_layout.addWidget(self.progress_label)
        self.quiz_layout.addStretch(1)
        self.quiz_layout.addWidget(self.question_widget)
        self.quiz_layout.addStretch(1)
        self.quiz_layout.addWidget(self.answers_widget)
        self.quiz_layout.addStretch(1)
        self.quiz_layout.addWidget(self.indicator_label)
        self.quiz_layout.addStretch(1)

        self.central_layout.addLayout(self.quiz_layout)
        self.start_new_question()

    def update_fixed_question_progress_label(self):
        """Update progress display for Fixed Question Mode."""
        if self.mode == "fixed_question":
            self.progress_label.setText(
                f"{self.current_question}/{self.total_questions}"
            )

    def clear_layout(self, layout: QVBoxLayout):
        """Utility to clear a layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if widget := item.widget():
                    widget.setParent(None)
                elif nested_layout := item.layout():
                    self.clear_layout(nested_layout)

    def show_results(self):
        """Display the results after the quiz or countdown ends."""
        self.clear_layout(self.central_layout)

        self.results_layout = QVBoxLayout()
        self.result_label.setText(
            f"Results:\nYou completed {self.current_question - 1} question{'s' if self.current_question - 1 != 1 else ''}."
        )

        self.mode_selection_layout.addWidget(self.fixed_question_button)
        self.mode_selection_layout.addWidget(self.countdown_button)

        self.results_layout.addStretch(3)
        self.results_layout.addWidget(self.result_label)
        self.results_layout.addStretch(1)
        self.results_layout.addLayout(self.mode_selection_layout)
        self.results_layout.addStretch(3)

        self.central_layout.addLayout(self.results_layout)

    def check_answer(self, selected_answer, correct_answer):
        if self.mode == "fixed_question":
            if selected_answer == correct_answer:
                self.indicator_label.show_message("Correct! Well done.")
                self.indicator_label.setStyleSheet("color: green;")
                self.current_question += 1
                self.update_fixed_question_progress_label()
                if self.current_question <= self.total_questions:
                    self.start_new_question()
                else:
                    self.show_results()
            else:
                self.indicator_label.show_message("Wrong! Try again.")
                self.indicator_label.setStyleSheet("color: red;")
                self.answers_widget.disable_answer(selected_answer)
        elif self.mode == "countdown":
            if selected_answer == correct_answer:
                self.indicator_label.show_message("Correct! Well done.")
                self.indicator_label.setStyleSheet("color: green;")
                self.current_question += 1
                self.start_new_question()
            else:
                self.indicator_label.show_message("Wrong! Try again.")
                self.indicator_label.setStyleSheet("color: red;")
                self.answers_widget.disable_answer(selected_answer)


    def resize_lesson_widget(self):
        """Resize UI elements dynamically."""
        self.question_widget._resize_question_widget()
        self.answers_widget.resize_answers_widget()
        self._resize_results_label()
        self._resize_progress_label()
        self._resize_indicator_label()
        self._resize_back_button()
        self._resize_mode_buttons()

    def _resize_mode_buttons(self):
        """Resize mode buttons based on window size."""
        button_font_size = self.main_widget.width() // 50
        for button in [self.fixed_question_button, self.countdown_button]:
            button.setFixedHeight(self.main_widget.width() // 10)
            button.setFixedWidth(self.main_widget.width() // 4)
            button.setStyleSheet(f"font-size: {button_font_size}px;")

    def _resize_results_label(self):
        """Resize results label based on window size."""
        results_label_font_size = self.main_widget.width() // 50
        self.result_label.setStyleSheet(f"font-size: {results_label_font_size}px;")

    def _resize_progress_label(self):
        """Resize progress label based on window size."""
        progress_label_font_size = self.main_widget.width() // 60
        self.progress_label.setStyleSheet(f"font-size: {progress_label_font_size}px;")
