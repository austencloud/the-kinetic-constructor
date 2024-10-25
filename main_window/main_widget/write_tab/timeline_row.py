# timeline_row.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.editable_label import EditableLabel
from main_window.main_widget.write_tab.timeline_beat_container import (
    TimelineBeatContainer,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_scroll_area import (
        TimelineScrollArea,
    )


class TimelineRow(QWidget):
    def __init__(self, scroll_area: "TimelineScrollArea") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.timeline = scroll_area.timeline
        self.beats: list[TimelineBeatContainer] = []
        self.timestamp_label = None

        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        # Setup timestamp as a QLabel but make it editable when clicked
        self.timestamp_label = EditableLabel("0:00")  # Starting with 0:00 placeholder
        self.layout.addWidget(self.timestamp_label)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setLayout(self.layout)

    def setup_beats(self):
        """Create beat containers and add them to the layout."""
        for i in range(8):  # Example: 8 beats per row
            beat_container = TimelineBeatContainer(
                self, self.timeline.main_widget, i + 1
            )
            self.beats.append(beat_container)
            self.layout.addWidget(beat_container)

    def resize_row(self):
        """Resize each beat in the row."""
        for beat in self.beats:
            beat.resize_timeline_beat_container()
