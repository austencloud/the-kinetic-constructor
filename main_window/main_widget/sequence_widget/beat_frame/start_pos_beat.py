from typing import TYPE_CHECKING

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF

from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class StartPositionBeat(Beat):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
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
