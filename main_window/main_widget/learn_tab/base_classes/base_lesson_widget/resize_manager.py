from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_lesson_widget import BaseLessonWidget


class LessonResizeManager:
    """Handles the layout and resizing of widgets for the lesson."""

    def __init__(self, base_widget: "BaseLessonWidget"):
        self.lesson_widget = base_widget

    def resize_widgets(self):
        """Resize UI elements dynamically."""
        self._resize_start_over_button()




    def _resize_start_over_button(self):
        font_size = self.lesson_widget.main_widget.width() // 60
        self.lesson_widget.start_over_button.setStyleSheet(f"font-size: {font_size}px;")
        self.lesson_widget.start_over_button.setFixedSize(
            self.lesson_widget.main_widget.width() // 8,
            self.lesson_widget.main_widget.height() // 12,
        )
