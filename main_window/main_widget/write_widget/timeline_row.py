# timeline_row.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from main_window.main_widget.write_widget.editable_label import EditableLabel
from main_window.main_widget.write_widget.timeline_beat_container import (
    TimelineBeatContainer,
)

if TYPE_CHECKING:
    from .timeline import Timeline


class TimelineRow(QWidget):
    def __init__(self, timeline_widget: "Timeline") -> None:
        super().__init__(timeline_widget)
        self.timeline = timeline_widget
        self.beats: list[TimelineBeatContainer] = []
        self.timestamp_label = None

        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        # Setup timestamp as a QLabel but make it editable when clicked
        self.timestamp_label = EditableLabel("0:00")  # Starting with 0:00 placeholder
        self.layout.addWidget(self.timestamp_label)

        # Add initial beats
        for _ in range(8):
            self.add_beat()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def add_beat(self):
        beat_container = TimelineBeatContainer(self)
        self.beats.append(beat_container)
        self.layout.addWidget(beat_container)

    def resize_row(self):
        for beat in self.beats:
            beat.resize_timeline_beat_container()
