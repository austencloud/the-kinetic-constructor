import json
import os
from typing import TYPE_CHECKING, Union

from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from PyQt6.QtCore import QEvent, Qt, QDir

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
            - self.act_sheet.act_container.beat_scroll.verticalScrollBar().width()
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
            data_str = bytes(data).decode("utf-8")
            sequence_dict = json.loads(data_str)

            # Confirm data structure before processing
            if isinstance(sequence_dict, dict):
                self.populate_beats(sequence_dict)
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
        beats = sequence_data.get("sequence", [])
        start_index = self.find_next_available_beat_index()

        for i, beat_data in enumerate(beats):
            if i < 2:
                continue
            current_index = start_index + i
            if current_index % 8 == 0:
                cue = beat_data.get("cue", "")
                timestamp = beat_data.get("timestamp", "")
                self.add_cue_and_timestamp(current_index, cue, timestamp)

            self.populate_beat(current_index - 2, beat_data)

        # Save act immediately after each population
        self.save_act_to_json()

    def _collect_sequences(self):
        """Collect sequences including cues, timestamps, and step labels for saving."""
        sequences = []
        total_rows = (
            self.act_sheet.act_container.beat_scroll.act_beat_frame.layout_manager.calculate_total_rows()
        )

        for row in range(total_rows):
            # Get cue and timestamp for each row
            cue, timestamp = self.act_sheet.act_container.get_cue_timestamp_for_row(row)
            sequence_data = {
                "sequence_start_marker": row == 0,
                "cue": cue,
                "timestamp": timestamp,
                "beats": [],
            }

            # Retrieve each beat view in the current row
            beat_views = self.act_sheet.act_container.get_beats_in_row(row)
            for beat_view in beat_views:
                if not beat_view.is_populated():
                    continue
                beat_data = beat_view.extract_metadata()
                beat_data["step_label"] = self.beat_step_map[beat_view].label.text()
                sequence_data["beats"].append(beat_data)

            sequences.append(sequence_data)
        return sequences

    def save_act_to_json(self, filename="current_act.json"):
        """Save the current act to a JSON file in the acts directory."""
        act_data = {
            "title": self.act_sheet.act_header.get_title(),
            "prop_type": self.main_widget.prop_type.name,
            "grid_mode": self.main_widget.settings_manager.global_settings.get_grid_mode(),
            "sequences": self._collect_sequences(),
        }
        acts_dir = os.path.join(QDir.currentPath(), "acts")
        os.makedirs(acts_dir, exist_ok=True)
        file_path = os.path.join(acts_dir, filename)

        with open(file_path, "w") as f:
            json.dump(act_data, f, indent=4)
        print(f"Act saved to {file_path}")

    def find_next_available_beat_index(self) -> int:
        """Find the next empty beat index in the act to start the new sequence."""
        for index, beat_view in enumerate(self.beats):
            if not beat_view.is_populated():
                return index
        return len(self.beats)  # Start at the end if all beats are populated

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
            beat_view.beat.updater.update_pictograph(beat_data)
            beat_view.beat.pictograph_dict = beat_data
            self.add_step_label(beat_view, step_label_text)

    def add_step_label(self, beat_view: ActBeatView, label_text: str):
        """Attach step label to an individual beat view."""
        if beat_view in self.beat_step_map:
            step_label = self.beat_step_map[beat_view]
            step_label.label.setText(label_text)

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
                self.dropEvent(event)
                return True
        return super().eventFilter(source, event)
