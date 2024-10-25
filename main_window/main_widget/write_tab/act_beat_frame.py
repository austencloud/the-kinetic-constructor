# act_beat_frame.py
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from main_window.main_widget.sequence_widget.beat_frame.act_beat_view import ActBeatView
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import (
    QDrag,
    QDragEnterEvent,
    QDragMoveEvent,
    QDropEvent,
    QMouseEvent,
    QPaintEvent,
    QResizeEvent,
)
import json
from PyQt6.QtCore import QDataStream, QIODevice

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class ActBeatFrame(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__()
        self.write_tab = write_tab
        self.main_widget = write_tab.main_widget
        self.beat_views: List[ActBeatView] = []
        self.timestamps: List[QLabel] = []  # Holds timestamp labels
        self._setup_layout()

    def _setup_layout(self):
        # Using a grid layout for both timestamps and beats
        self.layout: QGridLayout = QGridLayout(self)
        self.setLayout(self.layout)

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a large grid of beats."""
        for row in range(num_rows):
            # Add timestamp for each row
            timestamp = QLabel(f"{row * 10}:00")  # Example: 0:00, 0:10, etc.
            self.timestamps.append(timestamp)
            self.layout.addWidget(timestamp, row, 0)  # Align in the first column

            # Add beats for the row
            for col in range(1, num_beats + 1):
                beat_view = ActBeatView(self, number=(row * num_beats) + col)
                self.beat_views.append(beat_view)
                self.layout.addWidget(beat_view, row, col)

    def resizeEvent(self, event):
        """Resize each beat and adjust layout dynamically."""
        for view in self.beat_views:
            view.resize_act_beat_view()
        super().resizeEvent(event)

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
