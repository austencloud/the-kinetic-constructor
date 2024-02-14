from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView

from widgets.sequence_widget.beat_frame.beat import BeatView

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import SequenceBeatFrame
    from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat


class StartPositionBeat(Pictograph):
    def __init__(
        self, main_widget: "MainWidget", beat_frame: "SequenceBeatFrame"
    ) -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.beat_frame = beat_frame


class StartPositionBeatView(BeatView):
    def __init__(self, beat_frame: "SequenceBeatFrame") -> None:
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.is_filled = False

    def set_start_pos(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos = start_pos
        self.setScene(self.start_pos)
        view_width = self.height()
        self.view_scale = view_width / self.start_pos.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
