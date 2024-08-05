from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from widgets.sequence_widget.SW_beat_frame.beat import BeatView
if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.SW_beat_frame.image_export_manager import (
        ImageExportManager,
    )

class BaseBeatFrame(QFrame):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.json_manager = main_widget.json_manager
        self.settings_manager = main_widget.main_window.settings_manager
        self.initialized = True
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")


    def _init_beats(self):
        self.beats = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()

    def _setup_components(self):
        pass

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def populate_beat_frame_from_json(self, current_sequence_json):
        pass


    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if not beat.is_filled:
                return i
        return None

    def adjust_layout_to_sequence_length(self):
        pass

    def get_current_word(self) -> str:
        word = ""
        for beat_view in self.beats:
            if beat_view.is_filled:
                word += beat_view.beat.letter.value
        return self.simplify_repeated_word(word)

    def simplify_repeated_word(self, word: str) -> str:
        # Function to check if the word can be constructed by repeating a pattern
        def can_form_by_repeating(s: str, pattern: str) -> bool:
            pattern_len = len(pattern)
            return all(s[i:i + pattern_len] == pattern for i in range(0, len(s), pattern_len))

        n = len(word)
        # Try to find the smallest repeating unit
        for i in range(1, n // 2 + 1):
            pattern = word[:i]
            if n % i == 0 and can_form_by_repeating(word, pattern):
                return pattern
        return word