from PyQt6.QtCore import QTimer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class QuizTimerManager:
    """Handles timer logic for the quiz."""

    def __init__(self, base_widget: "BaseLessonWidget"):
        self.base_widget = base_widget
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

    def start_timer(self, duration):
        """Start the quiz timer."""
        self.base_widget.quiz_time = duration
        self.timer.start(1000)

    def update_timer(self):
        """Update the quiz timer each second."""
        minutes, seconds = divmod(self.base_widget.quiz_time, 60)
        self.base_widget.progress_label.setText(
            f"Time Remaining: {minutes}:{seconds:02d}"
        )

        if self.base_widget.quiz_time > 0:
            self.base_widget.quiz_time -= 1
        else:
            self.timer.stop()
            self.base_widget.show_results()

    def stop_timer(self):
        """Stop the quiz timer."""
        if self.timer.isActive():
            self.timer.stop()
