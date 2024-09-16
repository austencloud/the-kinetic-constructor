from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QCheckBox
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import (
        Lesson1Widget,
    )


class Lesson1TrackerWidget(QWidget):
    total_questions = 30

    def __init__(self, lesson_1_widget: "Lesson1Widget"):
        super().__init__(lesson_1_widget)

        self.lesson_1_widget = lesson_1_widget
        self.main_widget = lesson_1_widget.main_widget
        self.total_questions = self.total_questions
        self.correct_answers = 0
        self.incorrect_answers = 0

        # Timer tracking
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.elapsed_time = 0  # Time in seconds
        self.timer_running = False

        # Layout setup
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Create widgets
        self.correct_label = QLabel(
            f"Correct Answers: {self.correct_answers}/{self.total_questions}"
        )
        self.incorrect_label = QLabel(f"Incorrect Answers: {self.incorrect_answers}")
        self.timer_label = QLabel("Elapsed Time: 0s")

        self.labels = [self.correct_label, self.incorrect_label, self.timer_label]

        self.timer_checkbox = QCheckBox("Enable Timer")

        # Connect the timer toggle
        self.timer_checkbox.stateChanged.connect(self.toggle_timer)

        # Add widgets to the layout
        self.layout.addStretch(1)
        self.layout.addWidget(self.correct_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.incorrect_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.timer_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.timer_checkbox)
        self.layout.addStretch(1)

    def increment_correct(self):
        self.correct_answers += 1
        self.correct_label.setText(
            f"Correct Answers: {self.correct_answers}/{self.total_questions}"
        )
        if self.correct_answers >= self.total_questions:
            self.complete_quiz()

    def increment_incorrect(self):
        self.incorrect_answers += 1
        self.incorrect_label.setText(f"Incorrect Answers: {self.incorrect_answers}")

    def toggle_timer(self, state):
        if state == Qt.CheckState.Checked:
            self.start_timer()
        else:
            self.stop_timer()

    def start_timer(self):
        self.elapsed_time = 0
        self.timer_running = True
        self.timer.start(1000)  # Update every second

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False

    def update_time(self):
        if self.timer_running:
            self.elapsed_time += 1
            self.timer_label.setText(f"Elapsed Time: {self.elapsed_time}s")

    def complete_quiz(self):
        self.stop_timer()

    def resize_tracker_widget(self):
        self.setFixedWidth(self.main_widget.width() // 4)
        self._resize_labels()

    def _resize_labels(self):
        font_size = self.main_widget.width() // 60
        for label in self.labels:
            label.setStyleSheet(f"font-size: {font_size}px;")
        self.timer_checkbox.setStyleSheet(f"font-size: {font_size}px;")
