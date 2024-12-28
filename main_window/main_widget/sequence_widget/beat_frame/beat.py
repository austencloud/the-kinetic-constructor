from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsTextItem
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.beat_grabber import BeatGrabber
from .beat_number_manager import BeatNumberManager
from .beat_reversal_manager import BeatReversalManager

if TYPE_CHECKING:
    from .beat_view import BeatView
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class Beat(BasePictograph):
    def __init__(
        self, beat_frame: "SequenceWidgetBeatFrame", duration: Union[int, float] = 1
    ):
        super().__init__(beat_frame.main_widget)
        self.main_widget = beat_frame.main_widget
        self.reversal_symbol_manager = BeatReversalManager(self)
        self.number_manager = BeatNumberManager(self)
        self.grabber = BeatGrabber(self)

        self.view: "BeatView" = None
        self.beat_number_item: QGraphicsTextItem = None
        self.duration = duration
        self.is_placeholder = False
        self.parent_beat = None
        self.beat_number = 0
        self.blue_reversal = False
        self.red_reversal = False
