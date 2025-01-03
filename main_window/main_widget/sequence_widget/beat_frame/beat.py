from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.beat_grabber import BeatGrabber
from main_window.main_widget.sequence_widget.beat_frame.beat_start_text_manager import (
    BeatStartTextItem,
)
from .beat_number_item import BeatNumberItem
from .beat_reversal_manager import BeatReversalGlyph
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )
    from .beat_view import BeatView


class Beat(BasePictograph):
    view: "BeatView" = None
    is_placeholder = False
    parent_beat = None
    beat_number = 0
    blue_reversal = False
    red_reversal = False

    def __init__(
        self, beat_frame: "SequenceWidgetBeatFrame", duration: Union[int, float] = 1
    ):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.reversal_glyph = BeatReversalGlyph(self)
        self.number_item = BeatNumberItem(self)
        self.grabber = BeatGrabber(self)
        self.duration = duration
        self.start_text_item = BeatStartTextItem(self)
