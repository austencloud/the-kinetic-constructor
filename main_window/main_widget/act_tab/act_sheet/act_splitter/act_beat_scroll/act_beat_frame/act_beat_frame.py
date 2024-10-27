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
from main_window.main_widget.act_tab.act_sheet.act_splitter.act_beat_scroll.act_beat_frame.act_step_label import (
    ActStepLabel,
)
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
        self.step_labels: list[ActStepLabel] = []
        self.beat_step_map: dict[ActBeatView, ActStepLabel] = (
            {}
        )  # Dictionary for beat-step mapping

        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.layout_manager.setup_layout()
        self.init_act(self.act_sheet.DEFAULT_COLUMNS, self.act_sheet.DEFAULT_ROWS)

    def init_act(self, num_beats: int, num_rows: int):
        """Initialize the act with a grid of beats and labels."""
        self.num_columns = num_beats
        for row in range(num_rows):
            for col in range(num_beats):
                # Create and add each beat view
                beat_view = ActBeatView(self)
                beat_view.setCursor(Qt.CursorShape.PointingHandCursor)
                self.beats.append(beat_view)
                self.layout.addWidget(beat_view, row * 2, col)
                beat_number = col + 1
                beat_view.add_beat_number(beat_number)

                # Create and add each step label
                step_label = ActStepLabel(self, "")
                self.step_labels.append(step_label)
                self.layout.addWidget(step_label, row * 2 + 1, col)

                # Map the beat view to its associated step label
                self.beat_step_map[beat_view] = step_label

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

        for label in self.step_labels:
            label.resize_step_label()

    def dragEnterEvent(self, event: "QDragEnterEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event: "QDragMoveEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            event.acceptProposedAction()

    def dropEvent(self, event: "QDropEvent"):
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            stream = QDataStream(data, QIODevice.OpenModeFlag.ReadOnly)
            sequence_data = stream.readQString()

            sequence_dict = json.loads(sequence_data)
            self.handle_dropped_sequence(sequence_dict)

            event.acceptProposedAction()

    def handle_dropped_sequence(self, sequence_data):
        print("Dropped sequence data:", sequence_data)
