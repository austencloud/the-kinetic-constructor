from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from main_window.main_widget.write_tab.timestamp import Timestamp
from main_window.main_widget.write_tab.timeline_beat_container import (
    TimelineBeatContainer,
)
import json

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

        self.setAcceptDrops(True)  # Enable drop events
        self._setup_layout()
        self._setup_components()

    def _setup_components(self):
        self.timestamp_label = Timestamp("0:00")  # Starting with 0:00 placeholder
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
            beat_container.setAcceptDrops(True)  # Enable each beat to accept drops
            self.beats.append(beat_container)
            self.layout.addWidget(beat_container)

    def dragEnterEvent(self, event: QDropEvent):
        """Handle drag enter to show valid drop indicator."""
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()  # Accept only if the correct format
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop event to add the sequence to the timeline."""
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            metadata = json.loads(str(data, "utf-8"))

            # Process and apply the dropped sequence metadata
            print(f"Sequence metadata dropped: {metadata}")

            # Example: Apply the metadata to the first available beat
            for beat in self.beats:
                if not beat.is_filled:
                    beat.set_pictograph(metadata)  # Set the sequence data
                    break
            event.acceptProposedAction()
        else:
            event.ignore()

    def get_last_filled_beat(self):
        """Get the last filled beat in the row."""
        for beat in reversed(self.beats):
            if beat.is_filled:
                return beat
        return self.beats[0]

    def resize_row(self):
        """Resize each beat and the timestamp label in the row."""
        parent_width = self.scroll_area.timeline.write_tab.width()
        self.timestamp_label.resize_timestamp(parent_width)  # Resize timestamp label
        for beat in self.beats:
            beat.resize_timeline_beat_container()  # Resize each beat container
