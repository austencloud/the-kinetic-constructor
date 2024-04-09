from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from widgets.sequence_widget.sequence_widget_beat_frame.beat_deletion_manager import (
    BeatDeletionManager,
)
from widgets.sequence_widget.sequence_widget_beat_frame.beat_frame_image_export_manager import (
    BeatFrameImageExportManager,
)
from widgets.sequence_widget.sequence_widget_beat_frame.beat_frame_print_manager import (
    BeatFramePrintManager,
)
from widgets.sequence_widget.sequence_widget_beat_frame.beat_selection_overlay import (
    SequenceWidgetBeatSelectionOverlay,
)
from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
    StartPositionBeat,
)
from widgets.sequence_widget.sequence_widget_beat_frame.start_pos_beat import (
    StartPositionBeatView,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from widgets.sequence_widget.sequence_widget_beat_frame.beat import BeatView


class SequenceWidgetBeatFrame(QFrame):

    COLUMN_COUNT = 5
    ROW_COUNT = 4

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.main_widget = sequence_widget.main_widget
        self.current_sequence_json_handler = (
            self.main_widget.json_manager.current_sequence_json_handler
        )
        self.sequence_widget = sequence_widget
        self.top_builder_widget = sequence_widget.top_builder_widget
        self.beats: list[BeatView] = []
        self._setup_components()
        self._setup_layout()
        self._populate_beat_frame()

    def _populate_beat_frame(self) -> None:
        for i in range(1, self.COLUMN_COUNT):
            self._add_beat_to_layout(0, i)

        for j in range(1, 4):
            for i in range(
                1,
                self.COLUMN_COUNT,
            ):
                self._add_beat_to_layout(j, i)

    def _add_beat_to_layout(self, row: int, col: int, number=None) -> None:
        beat_view = BeatView(self, number)
        self.layout.addWidget(beat_view, row, col)
        self.beats.append(beat_view)

    def _setup_components(self) -> None:
        self.selection_manager = SequenceWidgetBeatSelectionOverlay(self)
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(self.main_widget, self)
        self.beat_deletion_manager = BeatDeletionManager(self)
        self.export_manager = BeatFrameImageExportManager(self)
        self.print_sequence_manager = BeatFramePrintManager(self)

    def _setup_layout(self) -> None:
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.start_pos_view, 0, 0)

    def keyPressEvent(self, event: "QKeyEvent") -> None:
        if event.key() == Qt.Key.Key_Delete or event.key() == Qt.Key.Key_Backspace:
            self.beat_deletion_manager.delete_selected_beat()
        else:
            super().keyPressEvent(event)

    def delete_selected_beat(self) -> None:
        self.beat_deletion_manager.delete_selected_beat()

    def add_scene_to_sequence(self, new_beat: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
            self.current_sequence_json_handler.update_current_sequence_file_with_beat(
                self.beats[next_beat_index]
            )

    def find_next_available_beat(self) -> int:
        for i, beat in enumerate(self.beats):
            if beat.scene() is None or beat.scene().items() == []:
                return i
        return None

    def get_last_filled_beat(self) -> BeatView:
        for beat_view in reversed(self.beats):
            if beat_view.is_filled:
                return beat_view
        return self.beats[0]

    def get_current_word(self) -> str:
        """
        This should go through the beats one by one and grab their letters, concatenating them to a word
        For the start pos, you can put the start pos letter plus _ to indicate the start of a word followed by the rest of the letters
        This can be achieved by getting pictograph.letter

        """

        word = ""
        for beat_view in self.beats:
            if beat_view.is_filled:
                word += beat_view.beat.letter.value
        # word += "_"
        # last_beat = self.get_last_filled_beat()
        # end_pos = last_beat.beat.get.end_pos_letter()
        # word += end_pos
        return word

    def on_beat_adjusted(self) -> None:
        current_sequence_json = (
            self.current_sequence_json_handler.load_current_sequence_json()
        )
        self.propogate_turn_adjustment(current_sequence_json)
        # self.main_widget.top_builder_widget.builder_toolbar.sequence_builder.option_picker.update_option_picker()

    def propogate_turn_adjustment(self, current_sequence_json) -> None:
        for i, entry in enumerate(current_sequence_json):
            if i == 0:
                self.update_start_pos_from_current_sequence_json(entry)
            else:
                beat = self.beats[i - 1].beat
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
        beat_view_size = int((self.width() // (self.COLUMN_COUNT)) * 0.75)
        for view in self.beats + [self.start_pos_view]:
            view.setMinimumWidth(beat_view_size)
            view.setMaximumWidth(beat_view_size)
            view.setMinimumHeight(beat_view_size)
            view.setMaximumHeight(beat_view_size)
            view.resetTransform()
            if view.scene():
                view.fitInView(
                    view.scene().sceneRect(), Qt.AspectRatioMode.KeepAspectRatio
                )