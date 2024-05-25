from typing import TYPE_CHECKING

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsScene
from PyQt6.QtCore import QPointF, Qt
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import (
        SW_BeatFrame,
    )


class StartPositionBeat(Beat):
    def __init__(self, beat_frame: "SW_BeatFrame") -> None:
        super().__init__(beat_frame)
        self.main_widget = beat_frame.main_widget
        self.beat_frame = beat_frame

    def add_start_text(self) -> None:
        start_text_item = QGraphicsTextItem("Start")
        start_text_item.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))
        text_padding = self.height() // 28
        start_text_item.setPos(QPointF(text_padding, text_padding))
        if self.view and self.view.scene():
            self.view.scene().addItem(start_text_item)


class StartPositionBeatView(BeatView):
    def __init__(self, beat_frame: "SW_BeatFrame") -> None:
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
