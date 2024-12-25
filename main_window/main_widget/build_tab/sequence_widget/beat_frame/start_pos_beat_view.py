from typing import TYPE_CHECKING


from main_window.main_widget.build_tab.sequence_widget.beat_frame.beat_view import (
    BeatView,
)
from main_window.main_widget.build_tab.sequence_widget.beat_frame.start_pos_beat import (
    StartPositionBeat,
)


if TYPE_CHECKING:
    from main_window.main_widget.build_tab.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class StartPositionBeatView(BeatView):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        super().__init__(beat_frame)
        self.is_start_pos = True
        self._setup_blank_beat()
        self.is_filled = False

    def _setup_blank_beat(self):
        self.blank_beat = StartPositionBeat(self.beat_frame)
        self.set_start_pos(self.blank_beat)
        self.blank_beat.grid.hide()

    def set_start_pos(self, start_pos: "StartPositionBeat") -> None:
        self.start_pos = self.beat = start_pos
        self.is_filled = True
        self.start_pos.view = self
        self.setScene(self.start_pos)
        view_width = self.height()
        self.view_scale = view_width / self.start_pos.width()
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.start_pos.add_start_text()
