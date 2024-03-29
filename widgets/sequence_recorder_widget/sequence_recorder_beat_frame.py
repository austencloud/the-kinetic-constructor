from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from widgets.sequence_recorder_widget.sequence_recorder_beat_selection_manager import SequenceRecorderBeatSelectionManager
from widgets.sequence_widget.sequence_beat_frame.beat_deletion_manager import (
    BeatDeletionManager,
)
from widgets.sequence_widget.sequence_beat_frame.beat_selection_manager import (
    SequenceBuilderBeatSelectionManager,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_widget import (
        SequenceRecorderWidget,
    )
    from widgets.sequence_recorder_widget.sequence_recorder_widget import MainWidget

from widgets.sequence_widget.sequence_beat_frame.beat import Beat, BeatView


class SequenceRecorderBeatFrame(QFrame):
    COLUMN_COUNT = 4
    ROW_COUNT = 4

    def __init__(self, sequence_recorder_widget: "SequenceRecorderWidget") -> None:
        super().__init__()
        self.sequence_recorder_widget = sequence_recorder_widget
        self.main_widget: "MainWidget" = sequence_recorder_widget.main_widget
        self.current_sequence_json_handler = (
            self.main_widget.json_manager.current_sequence_json_handler
        )
        self.beat_views: list[BeatView] = []
        self._setup_components()
        self._setup_layout()
        self._populate_beat_frame_with_views()

    def _populate_beat_frame_with_views(self) -> None:
        for j in range(self.ROW_COUNT):
            for i in range(self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)

    def _setup_components(self) -> None:
        self.selection_manager = SequenceRecorderBeatSelectionManager(self)
        self.beat_deletion_manager = BeatDeletionManager(self)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter
        )

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)

    def delete_selected_beat(self) -> None:
        self.beat_deletion_manager.delete_selected_beat()

    def _add_beat_to_layout(self, row: int, col: int) -> None:
        beat_view = BeatView(self)
        self.layout.addWidget(beat_view, row, col)
        self.beat_views.append(beat_view)

    def add_scene_to_sequence(self, new_beat: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beat_views[next_beat_index].set_pictograph(new_beat)
            self.current_sequence_json_handler.update_current_sequence_file_with_beat(
                self.beat_views[next_beat_index]
            )

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beat_views):
            if beat.scene() is None or beat.scene().items() == []:
                return i
        return None

    def get_last_filled_beat(self) -> BeatView:
        for beat_view in reversed(self.beat_views):
            if beat_view.is_filled:
                return beat_view
        return self.beat_views[0]

    def on_beat_adjusted(self) -> None:
        current_sequence_json = (
            self.current_sequence_json_handler.load_current_sequence_json()
        )
        self.propogate_turn_adjustment(current_sequence_json)
        self.main_widget.builder_toolbar.sequence_builder.option_picker.update_option_picker()

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                self.update_start_pos_from_current_sequence_json(entry)
            else:
                beat = self.beat_views[i - 1].beat
                if beat:
                    if beat.pictograph_dict != entry:
                        beat.updater.update_pictograph(entry)
                        QApplication.processEvents()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]

    def get_index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beat_views):
            if beat.is_selected:
                return i
        return 0

    def resize_beat_frame(self) -> None:
        beat_view_size = int(self.width() / (self.COLUMN_COUNT))
        for view in self.beat_views:
            view.setMinimumWidth(beat_view_size)
            view.setMaximumWidth(beat_view_size)
            view.setMinimumHeight(beat_view_size)
            view.setMaximumHeight(beat_view_size)
            view.resetTransform()
    
    def clear_beat_frame(self) -> None:
        for beat_view in self.beat_views:
            beat_view.setScene(None)
            beat_view.is_filled = False

    def populate_beat_frame_scenes_from_json(self) -> None:
        sequence_json = self.current_sequence_json_handler.load_current_sequence_json()
        self.clear_beat_frame()
        for pictograph_dict in sequence_json:
            if pictograph_dict.get("sequence_start_position"):
                continue
            beat = Beat(self.main_widget)
            beat.updater.update_pictograph(pictograph_dict)
            self.add_scene_to_sequence(beat)
            pictograph_key = (
                beat.main_widget.pictograph_key_generator.generate_pictograph_key(
                    pictograph_dict
                )
            )
            self.main_widget.pictograph_cache[pictograph_key] = beat
