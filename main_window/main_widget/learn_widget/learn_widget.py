# learn_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, QStackedLayout, QLabel, QScrollArea, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from data.constants import ANTI
from main_window.main_widget.codex_widget.codex_widget import CodexWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

def find_pictograph_dict(main_widget: "MainWidget", letter_str: str, start_pos: str, end_pos: str, blue_start_ori: str, red_start_ori: str) -> dict:
    """Search main_widget's preloaded pictograph_dicts for a given letter and conditions."""
    from Enums.letters import Letter
    target_letter = None
    for l in Letter:
        if l.value == letter_str:
            target_letter = l
            break
    if not target_letter:
        return None

    letter_dicts = main_widget.pictograph_dicts.get(target_letter, [])
    for pdict in letter_dicts:
        if pdict.get("start_pos") == start_pos and pdict.get("end_pos") == end_pos:
            blue_attrs = pdict.get("blue_attributes", {})
            red_attrs = pdict.get("red_attributes", {})
            if blue_attrs.get("start_ori") == blue_start_ori and red_attrs.get("start_ori") == red_start_ori:
                return pdict
    return None


class LearnWidget(QWidget):
    """Widget for the learning module, managing lesson selection and individual lessons."""

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.background_manager = None
        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )

        # We'll assume you have these widgets from your previous code:
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

        # Retrieve dictionaries for some example letters
        a_dict = find_pictograph_dict(
            self.main_widget,
            letter_str="A",
            start_pos="alpha1",
            end_pos="alpha3",
            blue_start_ori="in",
            red_start_ori="in"
        )
        b_dict = find_pictograph_dict(
            self.main_widget,
            letter_str="B",
            start_pos="alpha1",
            end_pos="alpha3",
            blue_start_ori="in",
            red_start_ori="in"
        )
        c_dict = find_pictograph_dict(
            self.main_widget,
            letter_str="C",
            start_pos="alpha1",
            end_pos="alpha3",
            blue_start_ori="in",
            red_start_ori="in",
            # blue_motion_type = "anti",
            # red_motion_type = "pro"
        )

        # Initial pictograph data (you can add more as needed)
        initial_pictograph_data = {
            "A": a_dict,
            "B": b_dict,
            "C": c_dict,
            # If you want more letters pre-loaded, find them similarly
        }

        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0,0,0,0)

        # Codex panel
        self.codex_shown = False
        self.codex_panel = CodexWidget(self, initial_pictograph_data)
        self.codex_panel.setFixedWidth(0)  # hidden initially

        # Right side with a top bar (Codex button) and stack_layout
        right_side = QWidget()
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(0,0,0,0)

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
        from main_window.main_widget.learn_widget.lesson_1.lesson_1_widget import Lesson1Widget
        return Lesson1Widget(self)

    def _create_lesson_2_widget(self):
        from main_window.main_widget.learn_widget.lesson_2.lesson_2_widget import Lesson2Widget
        return Lesson2Widget(self)

    def _create_lesson_3_widget(self):
        from main_window.main_widget.learn_widget.lesson_3.lesson_3_widget import Lesson3Widget
        return Lesson3Widget(self)
