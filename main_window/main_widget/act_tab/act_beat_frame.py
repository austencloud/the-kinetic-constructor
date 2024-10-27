from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from base_widgets.base_beat_frame import BaseBeatFrame
from main_window.main_widget.act_tab.act_beat_view import ActBeatView
from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
import json
from PyQt6.QtCore import QDataStream, QIODevice

from main_window.main_widget.sequence_widget.beat_frame.beat_selection_overlay import (
    BeatSelectionOverlay,
)
from main_window.main_widget.act_tab.timestamp import (
    Timestamp,
)
from main_window.main_widget.act_tab.act_beat_frame_layout_manager import (
    ActBeatFrameLayoutManager,
)

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_tab import ActTab
    from main_window.main_widget.act_tab.act_beat_scroll_area import ActBeatScrollArea


class ActBeatFrame(BaseBeatFrame):
    def __init__(self, beat_scroll_area: "ActBeatScrollArea"):
        super().__init__(beat_scroll_area.act_sheet.main_widget)
        self.act_tab = beat_scroll_area.act_sheet
        self.main_widget = self.act_tab.main_widget
        self.beats: list[ActBeatView] = []
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.layout_manager.setup_layout()

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a large grid of beats."""
        for row in range(num_rows):
            for col in range(num_beats):
                beat_view = ActBeatView(self)
                self.beats.append(beat_view)
                self.layout.addWidget(beat_view, row, col)
                beat_number = col + 1
                beat_view.add_beat_number(beat_number)

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def resize_act_beat_frame(self):
        """Resize each beat and adjust layout dynamically."""
        width_without_scrollbar = (
            self.width() - self.act_tab.beat_scroll_area.verticalScrollBar().width()
        )
        self.beat_size = int(width_without_scrollbar // 8)

        for view in self.beats:
            view.resize_act_beat_view()

    def dragEnterEvent(self, event: "QDragEnterEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()  # Accept the drag

    def dragMoveEvent(self, event: "QDragMoveEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()

    def dropEvent(self, event: "QDropEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
            sequence_data = stream.readQString()  # Deserialize the sequence data

            sequence_dict = json.loads(sequence_data)
            self.handle_dropped_sequence(sequence_dict)

            event.acceptProposedAction()

    def handle_dropped_sequence(self, sequence_data):
        print("Dropped sequence data:", sequence_data)
