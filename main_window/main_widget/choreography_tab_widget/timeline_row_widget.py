from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
from PyQt6.QtCore import Qt

from main_window.main_widget.choreography_tab_widget.editable_label import EditableLabel
from typing import TYPE_CHECKING

from main_window.main_widget.choreography_tab_widget.timeline_beat_widget import TimelineBeatWidget
if TYPE_CHECKING:
    from main_window.main_widget.choreography_tab_widget.timeline import Timeline

class TimelineRowWidget(QWidget):
    def __init__(self, timeline_widget: "Timeline") -> None:
        super().__init__(timeline_widget)
        self.timeline_widget = timeline_widget
        self.beats = []
        self.timestamp_label = None  # We will set this up later

        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        # Setup timestamp as a QLabel but make it editable when clicked
        self.timestamp_label = EditableLabel("0:00")  # Starting with 0:00 placeholder
        self.layout.addWidget(self.timestamp_label)

        # Add 8 blank beats (pictographs) to the row
        for _ in range(8):  
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

