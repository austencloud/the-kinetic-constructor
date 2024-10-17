from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtGui import QPainter

from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.base_lesson_widget import (
    BaseLessonWidget,
)
from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import Lesson1Widget
from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import Lesson2Widget
from main_window.main_widget.learn_widget.lesson_3.lesson_3_widget import Lesson3Widget
from main_window.main_widget.learn_widget.lesson_selector import LessonSelector

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from main_window.main_widget.main_widget import MainWidget


class LearnWidget(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        # QStackedLayout for managing different screens
        self.stack_layout = QStackedLayout()
        self.setLayout(self.stack_layout)

        # Lesson selection and individual lesson widgets
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = Lesson1Widget(self)
        self.lesson_2_widget = Lesson2Widget(self)
        self.lesson_3_widget = Lesson3Widget(self)

        # Add widgets to the stacked layout
        self.stack_layout.addWidget(self.lesson_selector)
        self.stack_layout.addWidget(self.lesson_1_widget)
        self.stack_layout.addWidget(self.lesson_2_widget)
        self.stack_layout.addWidget(self.lesson_3_widget)

        # Set the initial screen
        self.stack_layout.setCurrentWidget(self.lesson_selector)

        # self.background_manager = self.global_settings.setup_background_manager(self)

    def update_background_manager(self, bg_type: str):
        if self.background_manager:
            self.background_manager.stop_animation()
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.background_manager.start_animation()
        self.update()

    def show_lesson_selection_widget(self) -> None:
        """Show the lesson selection screen."""
        self.stack_layout.setCurrentWidget(self.lesson_selector)

    def start_lesson(self, lesson_number: int) -> None:
        """Start the specified lesson."""
        selected_mode = self.lesson_selector.mode_toggle_widget.get_selected_mode()
        lesson_widgets: list[BaseLessonWidget] = [
            self.lesson_1_widget,
            self.lesson_2_widget,
            self.lesson_3_widget,
        ]
        if lesson_number >= 1 and lesson_number <= len(lesson_widgets):
            lesson_widget = lesson_widgets[lesson_number - 1]
            lesson_widget.set_mode(selected_mode)
            self.stack_layout.setCurrentWidget(lesson_widget)

    def resize_learn_widget(self) -> None:
        """Dynamically adjust button sizes and font sizes based on window size."""
        self.lesson_1_widget.resize_lesson_widget()
        self.lesson_2_widget.resize_lesson_widget()
        self.lesson_3_widget.resize_lesson_widget()
        self.lesson_selector.resize_lesson_selector()

    # def paintEvent(self, event) -> None:
    #     """Draw the background using the background manager."""
    #     painter = QPainter(self)
    #     self.background_manager.paint_background(self, painter)

    # def showEvent(self, event):
    #     super().showEvent(event)
    #     self.background_manager.start_animation()

    # def hideEvent(self, event):
    #     super().hideEvent(event)
    #     if self.background_manager:
    #         self.background_manager.stop_animation()

    def resizeEvent(self, event) -> None:
        """Handle resize events for the widget."""
        super().resizeEvent(event)
        self.resize_learn_widget()
