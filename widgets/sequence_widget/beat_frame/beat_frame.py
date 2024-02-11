from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt
from widgets.sequence_widget.beat_frame.beat import Beat
from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat
from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeatView

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from widgets.sequence_widget.beat_frame.beat import BeatView


class BeatFrame(QFrame):
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
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.start_pos_view = StartPositionBeatView(self)
        self.start_pos = StartPositionBeat(main_widget, self)
        self.layout.addWidget(self.start_pos_view, 0, 0)

        for i in range(1, self.COLUMN_COUNT):
            self._add_beat_to_layout(0, i)

        for j in range(1, 4):
            for i in range(1, self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)

    def _add_beat_to_layout(self, row: int, col: int) -> None:
        beat_view = BeatView(self)
        beat = Beat(self.main_widget)
        beat_view.beat = beat
        self.layout.addWidget(beat_view, row, col)
        self.beats.append(beat_view)

    def add_start_pos(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos_view.set_start_pos(start_pos)

    def add_scene_to_sequence(self, new_beat: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beats[next_beat_index].set_pictograph(new_beat)

            
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
