from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout
from base_widgets.base_beat_frame import BaseBeatFrame
from main_window.main_widget.act_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_beat_view import (
    ActBeatView,
)
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
import json
from PyQt6.QtCore import QDataStream, QIODevice
from PyQt6.QtCore import Qt
from main_window.main_widget.act_tab.editable_label import EditableLabel
from main_window.main_widget.sequence_widget.beat_frame.beat_selection_overlay import (
    BeatSelectionOverlay,
)
from .act_beat_frame_layout_manager import ActBeatFrameLayoutManager

if TYPE_CHECKING:
    from ..act_beat_scroll import ActBeatScroll


class ActBeatFrame(BaseBeatFrame):
    layout: "QGridLayout"

    def __init__(self, beat_scroll_area: "ActBeatScroll"):
        super().__init__(beat_scroll_area.act_sheet.main_widget)
        self.act_sheet = beat_scroll_area.act_sheet
        self.main_widget = self.act_sheet.main_widget
        self.beats: list[ActBeatView] = []
        self.labels: list[EditableLabel] = []  # Add this line
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.layout_manager.setup_layout()
        self.init_act(self.act_sheet.DEFAULT_COLUMNS, self.act_sheet.DEFAULT_ROWS)

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a grid of beats and labels."""
        self.num_columns = num_beats  # Update the number of columns
        for row in range(num_rows):
            for col in range(num_beats):
                beat_view = ActBeatView(self)
                self.beats.append(beat_view)
                self.layout.addWidget(beat_view, row * 2, col)
                beat_number = col + 1
                beat_view.add_beat_number(beat_number)

                # Add an editable label under each beat
                label = EditableLabel(self, "", align=Qt.AlignmentFlag.AlignCenter)
                self.labels.append(label)
                self.layout.addWidget(label, row * 2 + 1, col)

    def resize_act_beat_frame(self):
        """Resize each beat and label, adjusting the layout dynamically."""
        width_without_scrollbar = (
            self.width()
            - self.act_sheet.splitter.beat_scroll.verticalScrollBar().width()
        )
        self.beat_size = int(width_without_scrollbar // self.num_columns)
        self.steps_label_height = self.beat_size // 2

        for view in self.beats:
            view.resize_act_beat_view()

        for label in self.labels:
            label.setFixedHeight(self.steps_label_height)  # Adjust as needed
            label.setFixedWidth(self.beat_size)
            label.resizeEvent(None)  # Trigger resize to adjust font size
            font_size = label.height() // 4
            font = label.font()
            font.setPointSize(font_size)
            label.setFont(font)
            label.edit.setFont(font)

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
