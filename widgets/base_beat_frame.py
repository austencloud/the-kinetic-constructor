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
        # self._init_beats()
        # self._setup_components()
        # self._setup_layout()

    def _init_beats(self):
        self.beats = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()

    def _setup_components(self):
        # Placeholder for components shared between derived classes
        pass

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def populate_beat_frame_from_json(self, current_sequence_json):
        # Logic to populate the beat frame from JSON data
        pass



    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if not beat.is_filled:
                return i
        return None

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.find_next_available_beat() or len(self.beats)
        self.layout_manager.configure_beat_frame(last_filled_index)
