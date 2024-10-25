from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor, QPalette
from main_window.main_widget.act_thumbnail_image_label import ActThumbnailImageLabel
from main_window.main_widget.sequence_widget.beat_frame.act_beat_view import ActBeatView
from main_window.main_widget.write_tab.timeline_row import TimelineRow
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from main_window.main_widget.write_tab.timestamp_label import TimestampLabel
from main_window.main_widget.write_tab.timeline_beat_container import TimelineBeatContainer
import json

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline import Timeline


class TimelineScrollArea(QScrollArea):
    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline)
        self.timeline = timeline
        self.main_widget = timeline.main_widget
        self.initialized = False
        self.setWidgetResizable(True)
        self.rows: dict[int, TimelineRow] = {}
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(0)
        self.content_widget.setLayout(self.content_layout)

        # Set the content widget inside the scroll area
        self.setWidget(self.content_widget)

    def add_default_rows(self, number_of_rows):
        """Add a specific number of timeline rows."""
        for _ in range(number_of_rows):
            self.add_row()

    def add_row(self):
        """Add a single row to the scroll area."""
        row_number = len(self.rows) + 1
        row = TimelineRow(self)  # Pass row number for beat numbers
        self.content_layout.addWidget(row)
        row.setup_beats()  # Call setup_beats after adding the row
        self.rows[len(self.rows)] = row


    def resize_timeline_scroll_area(self):
        for row in self.rows.values():
            row.resize_row()

    def resizeEvent(self, event):
        self.resize_timeline_scroll_area()
        super().resizeEvent(event)

    def dragEnterEvent(self, event: QDropEvent):
        """Accept drag event if the source is ActThumbnailImageLabel."""
        if isinstance(event.source(), ActThumbnailImageLabel):
            event.acceptProposedAction()

    # timeline_beat_container.py
    def dropEvent(self, event: QDropEvent):
        """Handle drop event to add the sequence to the timeline."""
        source = event.source()
        if isinstance(source, ActThumbnailImageLabel) and source.dragging_metadata:
            # Retrieve the sequence metadata directly from the source widget
            sequence_metadata = source.dragging_metadata.get("sequence", [])

            # Iterate over each item in the sequence to create and add pictographs
            for pictograph_data in sequence_metadata:
                pictograph_view = self.create_pictograph_view(pictograph_data)
                self.add_pictograph_to_timeline(pictograph_view)

            # Call function to update Act Browser with valid sequences
            self.update_act_browser_with_valid_sequences()

            event.acceptProposedAction()
        else:
            print("No valid metadata found for this drop event.")
            event.ignore()


    def create_pictograph_view(self, pictograph_data):
        """Convert pictograph data into a view."""
        # Use your pictograph creation logic here to generate a pictograph view
        return ActBeatView(
            self.timeline.write_tab.beat_frame, pictograph_data
        )

    def add_pictograph_to_timeline(self, pictograph_view):
        """Add a pictograph to the timeline."""
        # Append the pictograph view to the timeline
        next_beat =  self.get_next_empty_beat()
        next_beat.set_pictograph(pictograph_view)

    def update_act_browser_with_valid_sequences(self):
        """Filter Act Browser sequences to show only valid follow-up sequences."""
        # Get the last pictograph in the sequence to determine next valid options
        last_pictograph = self.get_last_pictograph_in_timeline()

        # Filter valid sequences based on the last pictograph in the sequence
        valid_sequences = self.get_valid_sequences(last_pictograph)

        # # Update Act Browser with only these valid sequences
        # self.act_browser.update_sequences(valid_sequences)

    def get_last_pictograph_in_timeline(self):
        """Retrieve the last pictograph in the timeline."""
        # Get the last pictograph view from the timeline
        last_pictograph = self.get_last_filled_beat()

        return last_pictograph

    def get_valid_sequences(self, last_pictograph):
        """Filter Act Browser sequences based on the last pictograph."""
        # Use your logic to filter valid sequences based on the last pictograph
        valid_sequences = []

        return valid_sequences

    def get_last_filled_beat(self):
        """Get the last filled beat in the row."""
        for timeline in self.rows.values():
            for beat in reversed(timeline.beats):
                if beat.is_filled:
                    return beat

    def get_next_empty_beat(self):
        """Get the next empty beat in the timeline."""
        for timeline in self.rows.values():
            for beat in timeline.beats:
                if not beat.is_filled:
                    return beat


    def set_act_browser(self, act_browser):
        """Set the Act Browser instance for the timeline."""
        self.act_browser = act_browser
