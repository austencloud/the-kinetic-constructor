from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.pictograph_view import PictographView
from .beat import Beat
from .start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatView(PictographView):
    is_start_pos = False
    is_filled = False
    is_selected = False
    is_start = False
    is_placeholder = False
    beat: "Beat" = None

    def __init__(self, beat_frame: "SequenceWidgetBeatFrame", number=None):
        super().__init__(beat_frame)
        self.number = number
        self.beat_frame = beat_frame
        self.setStyleSheet("border: none; border: 1px solid black;")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        self._setup_blank_beat()

    def _setup_blank_beat(self):
        self.blank_beat = StartPositionBeat(self.beat_frame)
        self.beat = self.blank_beat
        self.setScene(self.blank_beat)
        self.blank_beat.grid.hide()
        self.blank_beat.number_manager.add_beat_number()

    def set_beat(self, beat: "Beat", number: int) -> None:
        self.beat = beat
        self.beat.view = self
        self.is_filled = True
        self.beat.beat_number = number
        self.setScene(self.beat)
        self.beat.number_manager.add_beat_number(number)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.is_filled:
            self.beat_frame.selection_overlay.select_beat(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        beat_scene_size = (950, 950)
        view_size = self.size()

        self.view_scale = min(
            view_size.width() / beat_scene_size[0],
            view_size.height() / beat_scene_size[1],
        )
        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
