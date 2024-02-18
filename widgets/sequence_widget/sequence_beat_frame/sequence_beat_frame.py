import json
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from widgets.sequence_widget.sequence_beat_frame.beat import Beat
from widgets.sequence_widget.sequence_beat_frame.beat_selection_overlay import (
    BeatSelectionManager,
)
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import StartPositionBeat
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import (
    StartPositionBeatView,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView


class BeatDeletionManager:
    def __init__(self, sequence_beat_frame: "SequenceBeatFrame"):
        self.beat_frame = sequence_beat_frame
        self.beats = sequence_beat_frame.beats
        self.start_pos_view = self.beat_frame.start_pos_view
        self.GR_pictograph_view = (
            self.beat_frame.sequence_widget.sequence_modifier.graph_editor.GE_pictograph_view
        )
        self.sequence_builder = (
            self.beat_frame.sequence_widget.main_widget.main_tab_widget.sequence_builder
        )
        self.selection_manager = self.beat_frame.selection_manager

    def delete_selected_beat(self):
        selected_beat = self.beat_frame.selection_manager.get_selected_beat()

        if selected_beat.__class__ == StartPositionBeatView:
            self.start_pos_view.setScene(None)
            self.start_pos_view.is_filled = False
            self.GR_pictograph_view.set_to_blank_grid()
            for beat in self.beats:
                self.delete_beat(beat)
            self.selection_manager.deselect_beat()
            self.beat_frame.clear_current_sequence_file()
            self.sequence_builder.current_pictograph = None
            self.sequence_builder.reset_to_start_pos_picker()
            self.sequence_builder.option_picker.update_option_picker()

        elif selected_beat:
            if selected_beat == self.beats[0]:
                self.selection_manager.select_beat(self.start_pos_view)
                last_beat = self.start_pos_view
                self.sequence_builder.current_pictograph = self.start_pos_view.beat
                self.delete_beat(selected_beat)
                for i in range(
                    self.beats.index(selected_beat),
                    len(self.beats),
                ):
                    self.delete_beat(self.beats[i])
                self.beat_frame.clear_current_sequence_file_except_for_start_pos()
                self.beat_frame.update_current_sequence_file()

            else:
                self.delete_beat(selected_beat)
                for i in range(self.beats.index(selected_beat), len(self.beats)):
                    self.delete_beat(self.beats[i])
                last_beat = self.beat_frame.get_last_beat()
                self.selection_manager.select_beat(last_beat)
                self.sequence_builder.current_pictograph = last_beat.beat
            self.beat_frame.update_current_sequence_file()
            self.sequence_builder.option_picker.update_option_picker()

    def delete_beat(self, beat_view: BeatView) -> None:
        beat_view.setScene(None)
        beat_view.is_filled = False


class SequenceBeatFrame(QFrame):
    COLUMN_COUNT = 5
    ROW_COUNT = 4

    def __init__(
        self,
        main_widget: "MainWidget",
        sequence_widget: "SequenceWidget",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.sequence_widget = sequence_widget
        self.beats: list[BeatView] = []
        self._setup_components(main_widget)
        self._setup_layout()
        self._populate_beat_frame()

    def _populate_beat_frame(self):
        for i in range(1, self.COLUMN_COUNT):
            self._add_beat_to_layout(0, i)

        for j in range(1, 4):
            for i in range(1, self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)

    def _setup_components(self, main_widget):
        self.selection_manager = BeatSelectionManager(self)
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(main_widget, self)
        self.beat_deletion_manager = BeatDeletionManager(self)

    def _setup_layout(self):
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        )
        self.layout.addWidget(self.start_pos_view, 0, 0)

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)

    def delete_selected_beat(self):
        self.beat_deletion_manager.delete_selected_beat()

    def _add_beat_to_layout(self, row: int, col: int) -> None:
        beat_view = BeatView(self)
        beat = Beat(self.main_widget)
        beat_view.beat = beat
        self.layout.addWidget(beat_view, row, col)
        self.beats.append(beat_view)

    def add_scene_to_sequence(self, new_beat: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beats[next_beat_index].set_pictograph(new_beat)
            self.selection_manager.select_beat(self.beats[next_beat_index])
        self.update_current_sequence_file()

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if beat.scene() is None or beat.scene().items() == []:
                return i
        return None

    def get_last_beat(self) -> BeatView:
        for beat in reversed(self.beats):
            if beat.scene() is not None and beat.scene().items() != []:
                return beat
        return self.beats[0]

    def load_sequence(self) -> list[dict]:
        with open("current_sequence.json", "r", encoding="utf-8") as file:
            sequence_data = json.load(file)
        return sequence_data

    def update_current_sequence_file(self):
        temp_filename = "current_sequence.json"
        sequence_data = self.load_sequence()
        last_beat_view = self.get_last_beat()
        if (
            hasattr(last_beat_view.beat.get, "pictograph_dict")
            and last_beat_view.is_filled
        ):
            last_pictograph_dict = last_beat_view.beat.get.pictograph_dict()
            sequence_data.append(last_pictograph_dict)
        with open(temp_filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

    def clear_current_sequence_file(self):
        with open("current_sequence.json", "w", encoding="utf-8") as file:
            file.write("[]")

    def clear_current_sequence_file_except_for_start_pos(self):
        sequence_data = self.load_sequence()
        sequence_data = sequence_data[:1]
        with open("current_sequence.json", "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

    def is_full(self) -> bool:
        return all(beat.is_filled for beat in self.beats)

    def resize_beat_frame(self):
        beat_view_width = int(self.width() / self.COLUMN_COUNT)
        for beat_view in self.beats:
            beat_view.setMaximumWidth(beat_view_width)
            beat_view.setMaximumHeight(beat_view_width)
            beat_view.view_scale = beat_view_width / beat_view.beat.width()
            beat_view.resetTransform()
            beat_view.scale(beat_view.view_scale, beat_view.view_scale)
            beat_view.beat.container.styled_border_overlay.resize_styled_border_overlay()

        self.start_pos_view.setMaximumWidth(beat_view_width)
        self.start_pos_view.setMaximumHeight(beat_view_width)
        self.setMaximumHeight(beat_view_width * self.ROW_COUNT)
