from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonLayoutManager:
    """Handles the layout and resizing of widgets for the lesson."""

    def __init__(self, base_widget: "BaseLessonWidget"):
        self.base_widget = base_widget

    def setup_layout(self):
        """Setup common UI layout."""
        self.base_widget.central_layout.addWidget(self.base_widget.progress_label)
        self.base_widget.central_layout.addStretch(1)
        self.base_widget.central_layout.addWidget(self.base_widget.question_widget)
        self.base_widget.central_layout.addStretch(1)
        self.base_widget.central_layout.addWidget(self.base_widget.answers_widget)
        self.base_widget.central_layout.addStretch(1)
        self.base_widget.central_layout.addWidget(self.base_widget.indicator_label)
        self.base_widget.central_layout.addStretch(1)

    def resize_widgets(self):
        """Resize UI elements dynamically."""
        self.base_widget.question_widget._resize_question_widget()
        self.base_widget.answers_widget.resize_answers_widget()
        self._resize_indicator_label()
        self._resize_back_button()
        self._resize_progress_label()
        self._resize_result_label()
        self._resize_start_over_button()
        self.base_widget.results_widget.resize_results_widget()

    def _resize_indicator_label(self):
        self.base_widget.indicator_label.setFixedHeight(
            self.base_widget.main_widget.height() // 20
        )
        font = self.base_widget.indicator_label.font()
        font.setPointSize(self.base_widget.main_widget.width() // 75)
        self.base_widget.indicator_label.setFont(font)

    def _resize_back_button(self):
        font_size = self.base_widget.main_widget.width() // 60
        self.base_widget.back_button.setFixedSize(
            self.base_widget.main_widget.width() // 8,
            self.base_widget.main_widget.height() // 12,
        )
        self.base_widget.back_button.setStyleSheet(f"font-size: {font_size}px;")

    def _resize_progress_label(self):
        font_size = self.base_widget.main_widget.width() // 75
        font = self.base_widget.progress_label.font()
        font.setPointSize(font_size)
        self.base_widget.progress_label.setFont(font)

    def _resize_result_label(self):
        font_size = self.base_widget.main_widget.width() // 60
        font = self.base_widget.result_label.font()
        font.setPointSize(font_size)
        self.base_widget.result_label.setFont(font)

    def _resize_start_over_button(self):
        font_size = self.base_widget.main_widget.width() // 60
        self.base_widget.start_over_button.setStyleSheet(f"font-size: {font_size}px;")
        self.base_widget.start_over_button.setFixedSize(
            self.base_widget.main_widget.width() // 8,
            self.base_widget.main_widget.height() // 12,
        )
