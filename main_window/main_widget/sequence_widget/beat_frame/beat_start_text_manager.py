from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.beat_grabber import BeatGrabber
from .beat_number_item import BeatNumberItem
from .....base_widgets.base_pictograph.glyphs.reversals_glyph import BeatReversalGlyph
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from .beat_view import BeatView


class BeatStartTextItem(QGraphicsTextItem):
    def __init__(self, beat: "Beat"):
        super().__init__("Start")
        self.beat = beat
        self.beat.addItem(self)

    def add_start_text(self):
        if self.beat.number_item:
            self.beat.number_item.setVisible(False)
        self.setVisible(True)
        self.setFont(QFont("Georgia", 60, QFont.Weight.DemiBold))
        text_padding = self.beat.height() // 28
        self.setPos(QPointF(text_padding, text_padding))
