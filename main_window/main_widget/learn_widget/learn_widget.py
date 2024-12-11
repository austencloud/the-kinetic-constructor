# learn_widget.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QFrame,
    QStackedLayout,
)
from PyQt6.QtGui import QFont

from main_window.main_widget.learn_widget.codex_widget.codex_data_manager import (
    CodexDataManager,
)

from .codex_widget.codex import Codex

if TYPE_CHECKING:
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

        # Initialize PictographDataManager
        self.codex_data_manager = CodexDataManager(self.main_widget)
        initial_codex_data = self.codex_data_manager.get_pictograph_data()

        # Lesson widgets
        self.lesson_selector = self._create_lesson_selector()
        self.lesson_1_widget = self._create_lesson_1_widget()
        self.lesson_2_widget = self._create_lesson_2_widget()
        self.lesson_3_widget = self._create_lesson_3_widget()

        self.stack_layout = QStackedLayout()
        self.stack_layout.addWidget(self.lesson_selector)
        self.stack_layout.addWidget(self.lesson_1_widget)
        self.stack_layout.addWidget(self.lesson_2_widget)
        self.stack_layout.addWidget(self.lesson_3_widget)
        self.stack_layout.setCurrentWidget(self.lesson_selector)

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Codex panel
        self.codex_shown = False
        self.codex_panel = Codex(self, initial_codex_data)
        self.codex_panel.setFixedWidth(0)  # Hidden initially

        # Right side with a top bar (Codex button) and stack_layout
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.codex_button = QPushButton("Codex", self)
        self.codex_button.setFixedHeight(30)
        font = QFont()
        font.setBold(True)
        self.codex_button.setFont(font)
        self.codex_button.clicked.connect(self.toggle_codex)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(self.codex_button)
        top_bar_layout.addStretch()

        right_layout.addLayout(top_bar_layout)
        content_frame = QFrame()
        content_frame.setLayout(self.stack_layout)
        right_layout.addWidget(content_frame)

        self.main_layout.addWidget(self.codex_panel)
        self.main_layout.addWidget(right_side)
        self.setLayout(self.main_layout)

    def toggle_codex(self):
        self.codex_shown = not self.codex_shown
        self.codex_panel.toggle_codex(self.codex_shown)

    def show_lesson_selection_widget(self) -> None:
        """Show the lesson selection screen."""
        self.stack_layout.setCurrentWidget(self.lesson_selector)

    def start_lesson(self, lesson_number: int) -> None:
        """Start the specified lesson."""
        lesson_widgets = [
            self.lesson_1_widget,
            self.lesson_2_widget,
            self.lesson_3_widget,
        ]
        if 1 <= lesson_number <= len(lesson_widgets):
            lesson_widget = lesson_widgets[lesson_number - 1]
            self.stack_layout.setCurrentWidget(lesson_widget)

    def update_background_manager(self, bg_type: str):
        if self.background_manager:
            self.background_manager.stop_animation()
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.background_manager.start_animation()
        self.update()

    # Placeholder methods for creating lesson widgets
    def _create_lesson_selector(self):
        from main_window.main_widget.learn_widget.lesson_selector import LessonSelector

        return LessonSelector(self)

    def _create_lesson_1_widget(self):
        from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import (
            Lesson1Widget,
        )

        return Lesson1Widget(self)

    def _create_lesson_2_widget(self):
        from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import (
            Lesson2Widget,
        )

        return Lesson2Widget(self)

    def _create_lesson_3_widget(self):
        from main_window.main_widget.learn_widget.lesson_3.lesson_3_widget import (
            Lesson3Widget,
        )

        return Lesson3Widget(self)
