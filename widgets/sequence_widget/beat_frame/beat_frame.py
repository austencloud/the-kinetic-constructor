from typing import TYPE_CHECKING, List
from PyQt6.QtGui import QResizeEvent

from PyQt6.QtWidgets import QGridLayout, QFrame, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from constants.string_constants import BLUE, RED
from widgets.sequence_widget.beat_frame.beat import Beat
from widgets.sequence_widget.beat_frame.start_position import StartPosition
from widgets.sequence_widget.beat_frame.start_position_view import StartPositionView


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from objects.pictograph.pictograph import Pictograph
    from widgets.sequence_widget.sequence_widget import SequenceWidget

from widgets.sequence_widget.beat_frame.beat_view import BeatView


class BeatFrame(QFrame):
    picker_updater: pyqtSignal = pyqtSignal(dict)
    COLUMN_COUNT = 5

    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        sequence_widget: "SequenceWidget",
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.pictograph = pictograph
        self.sequence_widget = sequence_widget
        self.beats: List[BeatView] = []
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.start_position_view = StartPositionView(self)
        self.start_position = StartPosition(main_widget, self)
        self.layout.addWidget(self.start_position_view, 0, 0)

        for i in range(1, self.COLUMN_COUNT):
            self._add_beat_to_layout(0, i)

        for j in range(1, 4):
            for i in range(1, self.COLUMN_COUNT):
                self._add_beat_to_layout(j, i)

    def _add_beat_to_layout(self, row: int, col: int):
        beat_view = BeatView(self)
        beat = Beat(self.main_widget, self)
        beat_view.beat = beat
        self.layout.addWidget(beat_view, row, col)
        self.beats.append(beat_view)

    def add_start_position(self, start_position: "StartPosition"):
        self.start_position_view.set_start_position(start_position)

    def add_scene_to_sequence(self, copied_scene: "Pictograph") -> None:
        next_beat_index = self.find_next_available_beat()
        if next_beat_index is not None:
            self.beats[next_beat_index].set_pictograph(copied_scene)
        new_motions = {
            "red_motion": copied_scene.motions[RED],
            "blue_motion": copied_scene.motions[BLUE],
        }

        self.picker_updater.emit(new_motions)

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

    def resize_beat_frame(self) -> None:
        total_width = self.width()

        beat_view_width = int(total_width / self.COLUMN_COUNT)
        beat_view_height = int(beat_view_width * 90 / 75)

        for beat_view in self.beats:
            beat_view.setMinimumSize(beat_view_width, beat_view_height)
            beat_view.setMaximumSize(beat_view_width, beat_view_height)

        self.start_position_view.setMinimumSize(beat_view_width, beat_view_height)
        self.start_position_view.setMaximumSize(beat_view_width, beat_view_height)

        self.layout.update()
