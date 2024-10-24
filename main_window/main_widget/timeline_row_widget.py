# timeline_row_widget.py
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from .timeline_beat_widget import TimelineBeatWidget

if TYPE_CHECKING:
    from .timeline_widget import TimelineWidget


class TimelineRowWidget(QWidget):
    def __init__(self, timeline_widget: "TimelineWidget") -> None:
        super().__init__(timeline_widget)
        self.timeline_widget = timeline_widget
        self.beats: List[TimelineBeatWidget] = []

        self._setup_layout()
        self._setup_components()

    def _setup_components(self):

        # Add time stamp label
        self.time_stamp_label = QLabel("0:00")  # Placeholder for time stamp
        self.layout.addWidget(self.time_stamp_label)

        # Add initial beats
        for _ in range(8):  # Default to 8 beats per row
            self.add_beat()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def add_beat(self):
        beat = TimelineBeatWidget(self)
        self.beats.append(beat)
        self.layout.addWidget(beat)

    def resize_row(self):
        for beat in self.beats:
            beat.resize_beat()
