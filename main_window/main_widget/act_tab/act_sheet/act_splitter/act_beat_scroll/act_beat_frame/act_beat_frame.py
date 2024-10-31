import json
from typing import TYPE_CHECKING, Union

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtCore import QEvent, Qt

from base_widgets.base_beat_frame import BaseBeatFrame
from .act_beat_view import ActBeatView
from .act_step_label import ActStepLabel
from ......sequence_widget.beat_frame.beat_selection_overlay import BeatSelectionOverlay
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
        self.beat_step_map: dict[ActBeatView, ActStepLabel] = {}
        self.selection_overlay = BeatSelectionOverlay(self)
        self.layout_manager = ActBeatFrameLayoutManager(self)
        self.layout_manager.setup_layout()
        self.init_act(self.act_sheet.DEFAULT_COLUMNS, self.act_sheet.DEFAULT_ROWS)
        self.setAcceptDrops(True)  # Inside ActBeatFrame __init__
        self.installEventFilter(self)

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
            - self.act_sheet.act_frame.beat_scroll.verticalScrollBar().width()
        )
        self.beat_size = int(width_without_scrollbar // self.num_columns)
        self.steps_label_height = int(self.beat_size * (2 / 3))

        for view in self.beats:
            view.resize_act_beat_view()

        for label in self.step_labels:
            label.resize_step_label()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            print("Drag Enter Event Triggered")
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            print("Drag Move Event Triggered")
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasFormat("application/sequence-data"):
            data = event.mimeData().data("application/sequence-data")
            data_str = bytes(data).decode(
                "utf-8"
            )  # Decode the data from bytes to string
            sequence_dict = json.loads(data_str)  # Parse the JSON string

            # Confirm data structure before processing
            if isinstance(sequence_dict, dict):
                self.populate_beats(
                    sequence_dict
                )  # Populate beats if metadata is valid
                event.acceptProposedAction()
            else:
                print("Error: Dropped data is not in expected dictionary format")
                event.ignore()  # Ignore invalid data
        else:
            event.ignore()

    def get_beat_number(self, beat_view: ActBeatView) -> int:
        """Get the beat number for a given beat view."""
        return self.beats.index(beat_view) + 1

    def populate_beats(self, sequence_data: dict):
        """Populate act beats with metadata from the sequence."""
        beats = sequence_data.get("beats", [])
        sequence_length = len(beats)

        for i, beat_data in enumerate(beats):
            # Add cues and timestamps for the start of each row (every 8 beats)
            if i % 8 == 0:
                cue = beat_data.get("cue", "")
                timestamp = beat_data.get("timestamp", "")
                self.add_cue_and_timestamp(i, cue, timestamp)

            # Populate each individual beat
            self.populate_beat(i, beat_data)

    def add_cue_and_timestamp(self, beat_index: int, cue: str, timestamp: str):
        """Attach cue and timestamp to the corresponding row."""
        row_index = beat_index // 8
        # Assuming each cue and timestamp applies to the start of each 8-beat row
        cue_label = f"{timestamp} - {cue}"
        # Here you'd set the cue/timestamp text within the UI element for the row

    def populate_beat(self, beat_index: int, beat_data: dict):
        """Populate an individual beat with its metadata."""
        if beat_index < len(self.beats):
            beat_view = self.beats[beat_index]
            step_label_text = beat_data.get("step_label", "")
            beat_view.populate_from_metadata(beat_data)
            self.add_step_label(beat_view, step_label_text)

    def add_step_label(self, beat_view: ActBeatView, label_text: str):
        """Attach step label to an individual beat view."""
        if beat_view in self.beat_step_map:
            step_label = self.beat_step_map[beat_view]
            step_label.setText(label_text)

    def handle_dropped_sequence(self, sequence_data):
        print("Dropped sequence data:", sequence_data)

    def eventFilter(
        self, source, event: Union[QDragEnterEvent, QDragMoveEvent, QDropEvent]
    ):
        if event.type() in (
            QEvent.Type.DragEnter,
            QEvent.Type.DragMove,
            QEvent.Type.Drop,
        ):
            print("Event caught in eventFilter:", event.type())
            if event.type() == QEvent.Type.DragEnter and event.mimeData().hasFormat(
                "application/sequence-data"
            ):
                print("Drag Enter Event Triggered in eventFilter")
                event.accept()
                return True
            elif event.type() == QEvent.Type.DragMove and event.mimeData().hasFormat(
                "application/sequence-data"
            ):
                print("Drag Move Event Triggered in eventFilter")
                event.accept()
                return True
            elif event.type() == QEvent.Type.Drop and event.mimeData().hasFormat(
                "application/sequence-data"
            ):
                print("Drop Event Triggered in eventFilter")
                self.dropEvent(
                    event
                )  # Explicitly call dropEvent to ensure it processes
                return True
        return super().eventFilter(source, event)
