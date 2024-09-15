from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QStackedLayout
from PyQt6.QtGui import QPainter

from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import Lesson1Widget
from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import Lesson2Widget
from main_window.main_widget.learn_widget.lesson_selector import LessonSelector


if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from main_window.main_widget.main_widget import MainWidget


class LearnWidget(QWidget):
    """Main widget to manage lesson selection and quizzes."""

    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        # Use QStackedLayout to manage different screens (lesson selection, quizzes)
        self.stack_layout = QStackedLayout()
        self.setLayout(self.stack_layout)

        # Initialize the different lesson screens
        self.lesson_selector = LessonSelector(self)
        self.lesson_1_widget = Lesson1Widget(self)
        self.lesson_2_widget = Lesson2Widget(self)

        # Add the different screens to the stack
        self.stack_layout.addWidget(self.lesson_selector)
        self.stack_layout.addWidget(self.lesson_1_widget)
        self.stack_layout.addWidget(self.lesson_2_widget)

        # Show the lesson selection screen by default
        self.stack_layout.setCurrentWidget(self.lesson_selector)

        # Initialize background manager and connect signals
        self.connect_background_manager()

    def connect_background_manager(self):
        """Connect to the background manager to maintain consistent backgrounds."""
        self.main_widget.main_window.settings_manager.background_changed.connect(
            self.update_background_manager
        )

    def update_background_manager(self, bg_type: str):
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.update()

    def show_lesson_selection_widget(self):
        """Show the lesson selection screen."""
        self.stack_layout.setCurrentWidget(self.lesson_selector)

    def start_lesson_1(self):
        """Start Lesson 1 quiz (Pictograph -> Letter)."""
        self.stack_layout.setCurrentWidget(self.lesson_1_widget)
        self.lesson_1_widget.start_new_question()

    def start_lesson_2(self):
        """Start Lesson 2 quiz (Letter -> Pictograph)."""
        self.stack_layout.setCurrentWidget(self.lesson_2_widget)
        self.lesson_2_widget.start_new_question()

    def resize_learn_widget(self) -> None:
        """Dynamically adjust button sizes and font sizes based on window size."""
        self.lesson_1_widget.resize_lesson_1_widget()
        self.lesson_2_widget.resize_lesson_2_widget()
        self.lesson_selector.resize_lesson_selector()

    def paintEvent(self, event):
        """Draw the background using the background manager."""
        if self.background_manager is None:
            self.background_manager = self.global_settings.setup_background_manager(
                self
            )
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def resizeEvent(self, event):
        """Handle resize events for the widget."""
        self.resize_learn_widget()
        self.update()
        super().resizeEvent(event)
