from typing import TYPE_CHECKING

from PyQt6.QtGui import QMouseEvent

from widgets.sequence_widget.beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.sequence_widget.beat_frame.beat_frame import SequenceBeatFrame
    from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat


class StartPositionBeat(Beat):
    def __init__(
        self, main_widget: "MainWidget", beat_frame: "SequenceBeatFrame"
    ) -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.beat_frame = beat_frame


class StartPositionBeatView(BeatView):
    def __init__(self, beat_frame: "SequenceBeatFrame") -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame)
        self.is_filled = False

    def set_start_pos_beat(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos = start_pos
        self.is_filled = True
        self.start_pos.view = self
        self.setScene(self.start_pos)
        view_width = self.height()
        self.view_scale = view_width / self.start_pos.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)

    def mousePressEvent(self, event: QMouseEvent | None) -> None:
        self.selection_overlay.select_beat(self)
        self.viewport().update()  # Force the viewport to update