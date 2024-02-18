import json
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.sequence_widget.sequence_beat_frame.beat import Beat
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import StartPositionBeat
from widgets.sequence_widget.sequence_beat_frame.start_pos_beat import (
    StartPositionBeatView,
)

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView


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
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        )
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(main_widget, self)
        self.layout.addWidget(self.start_pos_view, 0, 0)

        for i in range(1, self.COLUMN_COUNT):
            self._add_beat_to_layout(0, i)

        for j in range(1, 4):
            for i in range(1, self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)
        self.selected_beat_view = None

        # add black borders
        # self.setStyleSheet("border: 1px solid black;")

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

        # set self.height() to match the combined height of the beat views
        self.setMaximumHeight(beat_view_width * self.ROW_COUNT)
