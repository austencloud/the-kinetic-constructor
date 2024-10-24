# timeline_beat_widget.py
from typing import TYPE_CHECKING, Optional
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtGui import QMouseEvent, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
import json

if TYPE_CHECKING:
    from .timeline_row_widget import TimelineRowWidget
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView, Beat
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class TimelineBeatWidget(QFrame):
    def __init__(self, timeline_row: "TimelineRowWidget") -> None:
        super().__init__(timeline_row)
        self.timeline_row = timeline_row
        self.pictograph_view: Optional["BeatView"] = None

        self._setup_ui()
        self.setAcceptDrops(True)

    def _setup_ui(self):
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

    def set_pictograph(self, pictograph_view: "BeatView"):
        self.pictograph_view = pictograph_view
        # Clear any existing widgets
        for i in reversed(range(self.layout().count())):
            widget = self.layout().takeAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        # Display the pictograph within this widget
        self.layout().addWidget(pictograph_view)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if self.pictograph_view:
            # Open GraphEditor to edit this pictograph
            graph_editor = self.timeline_row.timeline_widget.choreography_tab.main_widget.sequence_widget.graph_editor
            graph_editor.show()
            # Load the pictograph into the GraphEditor
            graph_editor.pictograph_container.load_pictograph(self.pictograph_view.beat)
        else:
            super().mouseDoubleClickEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat('application/x-sequence'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        mime_data = event.mimeData()
        if mime_data.hasFormat('application/x-sequence'):
            sequence_data = mime_data.data('application/x-sequence')
            sequence = json.loads(bytes(sequence_data).decode('utf-8'))
            # Create pictograph from sequence
            self.set_pictograph_from_sequence(sequence)
            event.acceptProposedAction()
        else:
            event.ignore()

    def set_pictograph_from_sequence(self, sequence):
        # Use your existing method to create a Beat and BeatView from the sequence
        beat = Beat(self, duration=1)
        beat.updater.update_pictograph(sequence)
        beat_view = BeatView(self, beat=beat)
        self.set_pictograph(beat_view)

    def resize_beat(self):
        # Adjust size based on parent widget size
        pass
