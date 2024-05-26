from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGridLayout, QFrame, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent

from widgets.sequence_widget.SW_beat_frame_layout_manager import (
    SW_BeatFrameLayoutManager,
)
from .beat_deletion_manager import BeatDeletionManager
from .sequence_image_export_manager import SequenceImageExportManager
from .beat_frame_print_manager import BeatFramePrintManager
from .beat_selection_overlay import SequenceWidgetBeatSelectionOverlay
from .start_pos_beat import StartPositionBeat
from .start_pos_beat import StartPositionBeatView
from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from .beat import BeatView


class SW_BeatFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.main_widget = sequence_widget.main_widget
        self.current_sequence_json_handler = (
            self.main_widget.json_manager.current_sequence_json_handler
        )
        self.sequence_widget = sequence_widget
        self.top_builder_widget = sequence_widget.top_builder_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.sequence_changed = False
        self.setObjectName("beat_frame")
        self.setStyleSheet("QFrame#beat_frame { background: transparent; }")
        self._init_beats()
        self._setup_components()
        self._setup_layout()

    def _init_beats(self):
        self.beats = [BeatView(self, number=i + 1) for i in range(64)]
        for beat in self.beats:
            beat.hide()

    def _setup_components(self) -> None:
        self.selection_manager = SequenceWidgetBeatSelectionOverlay(self)
        self.layout_manager = SW_BeatFrameLayoutManager(self)
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self)
        self.beat_deletion_manager = BeatDeletionManager(self)
        self.export_manager = SequenceImageExportManager(self)
        self.print_sequence_manager = BeatFramePrintManager(self)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.start_pos_view, 0, 0)
        for i, beat in enumerate(self.beats):
            row, col = divmod(i, 8)
            self.layout.addWidget(beat, row + 1, col + 1)
        self.layout_manager.configure_beat_frame(16)

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)

    def delete_selected_beat(self) -> None:
        self.beat_deletion_manager.delete_selected_beat()

    def add_beat_to_sequence(self, new_beat: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()

        grow_sequence = self.settings_manager.get_grow_sequence()
        if grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.current_sequence_json_handler.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                self.sequence_widget.update_current_word()  # Update the current word
                if self.settings_manager.get_grow_sequence():
                    self.adjust_layout_to_sequence_length()
        elif not grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
                and self.beats[next_beat_index].isVisible()
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.current_sequence_json_handler.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                self.sequence_widget.update_current_word()

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if not beat.is_filled:
                return i
        return None

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.find_next_available_beat() or len(self.beats)
        self.layout_manager.configure_beat_frame(last_filled_index)

    def get_last_filled_beat(self) -> BeatView:
        for beat_view in reversed(self.beats):
            if beat_view.is_filled:
                return beat_view
        return self.beats[0]

    def get_current_word(self) -> str:
        word = ""
        for beat_view in self.beats:
            if beat_view.is_filled:
                word += beat_view.beat.letter.value
        return word

    def on_beat_adjusted(self) -> None:
        current_sequence_json = (
            self.current_sequence_json_handler.load_current_sequence_json()
        )
        self.propogate_turn_adjustment(current_sequence_json)

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                continue
            elif i == 1:
                self.update_start_pos_from_current_sequence_json(entry)
            elif i > 1:
                beat = self.beats[i - 2].beat
                if beat:
                    if beat.pictograph_dict != entry:
                        beat.updater.update_pictograph(entry)
                        QApplication.processEvents()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.start_pos_view.start_pos.updater.update_pictograph(entry)

    def get_index_of_currently_selected_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if beat.is_selected:
                return i
        return 0

    def resize_beat_frame(self) -> None:
        scrollbar_width = self.sequence_widget.scroll_area.verticalScrollBar().width()
        width = int(
            (
                self.sequence_widget.width()
                - self.sequence_widget.button_frame.width()
                - scrollbar_width
            )
            * 0.8
        )
        num_cols = max(1, self.layout.columnCount() - 1)
        if num_cols == 0:
            return
        beat_size = int(width / (5))
        for beat in self.beats:
            beat.setFixedSize(beat_size, beat_size)
        self.start_pos_view.setFixedSize(beat_size, beat_size)
        for beat in self.beats:
            beat.resize_beat_view()
        self.start_pos_view.resize_beat_view()
