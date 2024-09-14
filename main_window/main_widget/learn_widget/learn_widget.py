from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter

from main_window.main_widget.learn_widget.level_1_quiz_selector import (
    Level1QuizSelector,
)
from main_window.main_widget.learn_widget.level_1_0_quiz import Level_1_0_Quiz
from main_window.main_widget.learn_widget.level_selection_widget import (
    LevelSelectionWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.learn_widget import LearnWidget
    from main_window.main_widget.main_widget import MainWidget


class LearnWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        # Use QStackedLayout to manage different screens
        self.stack_layout = QStackedLayout()
        self.setLayout(self.stack_layout)

        # Initialize the different screens
        self.level_selection_widget = LevelSelectionWidget(self)
        self.level_1_quiz_selector = Level1QuizSelector(self)
        self.level_1_quiz = Level_1_0_Quiz(self)

        # Add to stack
        self.stack_layout.addWidget(self.level_selection_widget)
        self.stack_layout.addWidget(self.level_1_quiz_selector)
        self.stack_layout.addWidget(self.level_1_quiz)

        # Show the level selection widget by default
        self.stack_layout.setCurrentWidget(self.level_selection_widget)

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

    def show_level_selection_widget(self):
        """Show the level selection screen."""
        self.stack_layout.setCurrentWidget(self.level_selection_widget)

    def show_level_1_quiz_selector(self):
        """Show the Level 1 quiz selector."""
        self.stack_layout.setCurrentWidget(self.level_1_quiz_selector)

    def start_level_1_0_quiz(self):
        """Start the 1.0 quiz (Pictograph -> Letter)."""
        self.stack_layout.setCurrentWidget(self.level_1_quiz)
        self.level_1_quiz.start_new_question()

    def start_level_1_1_quiz(self):
        """Start the 1.1 quiz (Letter -> Pictograph)."""
        self.stack_layout.setCurrentWidget(self.level_1_quiz)
        self.level_1_quiz.start_new_question()

    def start_intermediate_module(self):
        print("Starting Intermediate Module")
        # Implement logic to handle starting intermediate module

    def start_advanced_module(self):
        print("Starting Advanced Module")
        # Implement logic to handle starting advanced module

    def resize_learn_widget(self) -> None:
        """Dynamically adjust button sizes and font sizes based on window size."""
        self.level_1_quiz_selector.resize_level_1_quiz_selector()
        self.level_1_quiz.resize_level_1_0_quiz()
        self.level_selection_widget.resize_level_selection_widget()

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