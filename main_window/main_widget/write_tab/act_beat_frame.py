from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from base_widgets.base_beat_frame import BaseBeatFrame
from main_window.main_widget.write_tab.act_beat_view import ActBeatView
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
import json
from PyQt6.QtCore import QDataStream, QIODevice

from main_window.main_widget.sequence_widget.beat_frame.beat_selection_overlay import (
    BeatSelectionOverlay,
)
from main_window.main_widget.write_tab.timestamp import (
    Timestamp,
)
from main_window.main_widget.write_tab.act_beat_frame_layout_manager import (
    ActBeatFrameLayoutManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class ActBeatFrame(BaseBeatFrame):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab.main_widget)
        self.write_tab = write_tab
        self.main_widget = write_tab.main_widget
        self.beats: list[ActBeatView] = []
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.layout_manager.setup_layout()

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a large grid of beats."""
        for row in range(num_rows):
            # Add beats for the row
            for col in range(num_beats):
                beat_view = ActBeatView(self)
                self.beats.append(beat_view)
                self.layout.addWidget(beat_view, row, col)
                beat_number = col + 1  # Number each beat in the row from 1 to 8
                beat_view.add_beat_number(beat_number)

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def resize_act_beat_frame(self):
        """Resize each beat and adjust layout dynamically."""
        width_without_scrollbar = (
            self.width() - self.write_tab.beat_scroll_area.verticalScrollBar().width()
        )
        self.beat_size = int(width_without_scrollbar // 8)

        for view in self.beats:
            view.resize_act_beat_view()  # Ensure that each beat is resized correctly



    def dragEnterEvent(self, event: "QDragEnterEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()  # Accept the drag

    def dragMoveEvent(self, event: "QDragMoveEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()
            # Highlight the row or show a preview where the user is dragging the pictograph
            self.highlight_row_under_cursor(event.pos())

    def highlight_row_under_cursor(self, pos):
        # Highlight the row under the cursor
        for row in range(len(self.timestamps)):
            timestamp = self.timestamps[row]
            if timestamp.geometry().contains(pos):
                timestamp.setStyleSheet("background-color: rgba(0, 0, 0, 0.1)")
            else:
                timestamp.setStyleSheet("background-color: transparent")

    def dropEvent(self, event: "QDropEvent"):
        # Extract metadata from the drop event
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
            sequence_data = stream.readQString()  # Deserialize the sequence data

            # You can now use sequence_data (in JSON format) to populate the act frame
            sequence_dict = json.loads(sequence_data)
            # Add logic to update the act with the dropped sequence
            self.handle_dropped_sequence(sequence_dict)

            event.acceptProposedAction()

    def handle_dropped_sequence(self, sequence_data):
        # Handle how the sequence data is applied to the Act Beat Frame
        print("Dropped sequence data:", sequence_data)
        # Add sequence to beat, display a preview, etc.
