from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonLayoutManager:
    """Handles the layout and resizing of widgets for the lesson."""

    def __init__(self, base_widget: "BaseLessonWidget"):
        self.lesson_widget = base_widget

    def setup_layout(self):
        """Setup common UI layout."""
        layout = self.lesson_widget.central_layout
        layout.addWidget(self.lesson_widget.progress_label)
        layout.addStretch(1)
        layout.addWidget(self.lesson_widget.question_widget)
        layout.addStretch(1)
        layout.addWidget(self.lesson_widget.answers_widget)
        layout.addStretch(1)
        layout.addWidget(self.lesson_widget.indicator_label)
        layout.addStretch(1)

    def resize_widgets(self):
        """Resize UI elements dynamically."""
        # self._resize_progress_label()
        # self._resize_result_label()
        self._resize_start_over_button()
        # self.lesson_widget.results_widget.resize_results_widget()

    # def _resize_progress_label(self):
    #     font_size = self.lesson_widget.main_widget.width() // 75
    #     font = self.lesson_widget.progress_label.font()
    #     font.setPointSize(font_size)
    #     self.lesson_widget.progress_label.setFont(font)

    # def _resize_result_label(self):
    #     font_size = self.lesson_widget.main_widget.width() // 60
    #     font = self.lesson_widget.result_label.font()
    #     font.setPointSize(font_size)
    #     self.lesson_widget.result_label.setFont(font)

    def _resize_start_over_button(self):
        font_size = self.lesson_widget.main_widget.width() // 60
        self.lesson_widget.start_over_button.setStyleSheet(f"font-size: {font_size}px;")
        self.lesson_widget.start_over_button.setFixedSize(
            self.lesson_widget.main_widget.width() // 8,
            self.lesson_widget.main_widget.height() // 12,
        )
