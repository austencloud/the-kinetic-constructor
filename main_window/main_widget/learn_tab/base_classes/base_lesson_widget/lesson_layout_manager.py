from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonLayoutManager:
    """Handles the layout and resizing of widgets for the lesson."""

    def __init__(self, lesson_widget: "BaseLessonWidget"):
        self.lesson_widget = lesson_widget

    def setup_central_layout(self):
        """Setup common UI layout."""
        central_layout = self.lesson_widget.central_layout
        central_layout.addWidget(self.lesson_widget.progress_label)
        central_layout.addStretch(1)
        central_layout.addWidget(self.lesson_widget.question_widget)
        central_layout.addStretch(1)
        central_layout.addWidget(self.lesson_widget.answers_widget)
        central_layout.addStretch(1)
        central_layout.addWidget(self.lesson_widget.indicator_label)
        central_layout.addStretch(1)
