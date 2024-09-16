from PyQt6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import QTimer, Qt
from ..base_classes.base_lesson_widget import BaseLessonWidget
from .lesson_2_question_generator import Lesson2QuestionGenerator
from .lesson_2_question_widget import Lesson2QuestionWidget
from .lesson_2_answers_widget import Lesson2AnswersWidget


class Lesson2Widget(BaseLessonWidget):
    """Lesson 2 widget for handling letter to pictograph matching and quiz logic."""

    def __init__(self, learn_widget):
        super().__init__(learn_widget)

        # Override question and answer widgets
        self.question_widget = Lesson2QuestionWidget(self)
        self.answers_widget = Lesson2AnswersWidget(self)
        self.question_generator = Lesson2QuestionGenerator(self)

        # UI Elements
        self.progress_label = self.create_label(alignment=Qt.AlignmentFlag.AlignCenter)
        self.result_label = self.create_label(alignment=Qt.AlignmentFlag.AlignCenter)

        # Timer
        self.quiz_timer = QTimer()  # For quiz duration (2 minutes)
        self.quiz_timer.timeout.connect(self.update_quiz_timer)

        # Other attributes
        self.total_questions = 5
        self.current_question = 1

    # --------------------------------------
    # Mode Setup
    # --------------------------------------
    def set_mode(self, mode: str) -> None:
        """Set the quiz mode (Fixed Questions or Countdown)."""
        self.mode = mode
        if self.mode == "Fixed Questions":
            self.start_fixed_question_mode()
        elif self.mode == "Countdown":
            self.start_countdown_mode()

    # --------------------------------------
    # Fixed Question Mode
    # --------------------------------------
    def start_fixed_question_mode(self):
        """Start the Fixed Question Mode by setting up the UI."""
        self.mode = "fixed_question"
        self.current_question = 1
        self.update_fixed_question_progress_label()

        if self.quiz_timer.isActive():
            self.quiz_timer.stop()
        self.prepare_quiz_ui()

    def update_fixed_question_progress_label(self):
        """Update progress display for Fixed Question Mode."""
        self.progress_label.setText(f"{self.current_question}/{self.total_questions}")

    # --------------------------------------
    # Countdown Mode
    # --------------------------------------
    def start_countdown_mode(self):
        """Start the Countdown Mode by setting up the UI."""
        self.mode = "countdown"
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

    # --------------------------------------
    # Quiz UI Preparation
    # --------------------------------------
    def prepare_quiz_ui(self):
        """Prepare and switch to the quiz interface layout."""
        self.clear_layout(self.central_layout)
        self.quiz_layout = self.create_quiz_layout()
        self.central_layout.addLayout(self.quiz_layout)
        self.start_new_question()

    def create_quiz_layout(self) -> QVBoxLayout:
        """Creates the layout for the quiz UI."""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        layout.addWidget(self.progress_label)
        layout.addStretch(1)
        layout.addWidget(self.question_widget)
        layout.addStretch(1)
        layout.addWidget(self.answers_widget)
        layout.addStretch(1)
        layout.addWidget(self.indicator_label)
        layout.addStretch(1)
        return layout

    # --------------------------------------
    # Results Display
    # --------------------------------------
    def show_results(self):
        """Display the results after the quiz or countdown ends."""
        self.clear_layout(self.central_layout)
        self.results_layout = self.create_results_layout()
        self.central_layout.addLayout(self.results_layout)

    def create_results_layout(self) -> QVBoxLayout:
        """Creates the layout for the results screen."""
        self.clear_layout(self.central_layout)
        layout = QVBoxLayout()
        self.result_label.setText(
            f"Results:\nYou completed {self.current_question - 1} question"
            f"{'s' if self.current_question - 1 != 1 else ''}."
        )

        layout.addStretch(1)
        layout.addWidget(self.result_label)
        layout.addStretch(1)
        return layout

    # --------------------------------------
    # Answer Checking
    # --------------------------------------
    def check_answer(self, selected_answer, correct_answer):
        """Check the answer and show feedback."""
        if selected_answer == correct_answer:
            self.indicator_label.show_message("Correct! Well done.")
            self.indicator_label.setStyleSheet("color: green;")
            self.current_question += 1

            if self.mode == "fixed_question":
                self.update_fixed_question_progress_label()
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

    # --------------------------------------
    # Utility Methods
    # --------------------------------------
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

    # --------------------------------------
    # Resizing Methods
    # --------------------------------------
    def resize_lesson_widget(self):
        """Resize UI elements dynamically."""
        self.question_widget._resize_question_widget()
        self.answers_widget.resize_answers_widget()
        self._resize_results_label()
        self._resize_progress_label()
        self._resize_indicator_label()
        self._resize_back_button()

    def _resize_results_label(self):
        """Resize results label based on window size."""
        self.result_label.setStyleSheet(
            f"font-size: {self.main_widget.width() // 50}px;"
        )

    def _resize_progress_label(self):
        """Resize progress label based on window size."""
        self.progress_label.setStyleSheet(
            f"font-size: {self.main_widget.width() // 60}px;"
        )
