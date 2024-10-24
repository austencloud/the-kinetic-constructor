from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.write_widget.editable_label import EditableLabel
from typing import TYPE_CHECKING

from main_window.main_widget.write_widget.timeline_beat_container import (
    TimelineBeatContainer,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_widget.timeline import Timeline


class TimelineRow(QWidget):
    def __init__(self, timeline_widget: "Timeline") -> None:
        super().__init__(timeline_widget)
        self.timeline = timeline_widget
        self.beats: list[TimelineBeatContainer] = []
        self.timestamp_label = None  # We will set this up later

        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        self.timestamp_label = EditableLabel("0:00")  # Starting with 0:00 placeholder
        self.layout.addWidget(self.timestamp_label, 1)

        for _ in range(8):
            self.add_beat()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.layout)

    def add_beat(self):
        beat_container = TimelineBeatContainer(self)
        self.beats.append(beat_container)
        self.layout.addWidget(beat_container, 1)

    def resize_row(self):
        self.timestamp_label.setMaximumWidth(self.width() // 10)
        for beat in self.beats:
            beat.resize_timeline_beat_container()
