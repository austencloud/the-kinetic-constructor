# cue_box.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt

from .cue_label.cue_label import CueLabel
from .timestamp.timestamp import Timestamp


if TYPE_CHECKING:
    from ..cue_frame import CueFrame


# cue_box.py
class CueBox(QWidget):
    def __init__(
        self, cue_frame: "CueFrame", timestamp_text: str, cue_label_text: str = ""
    ):
        super().__init__(cue_frame)
        self.cue_frame = cue_frame

        self.timestamp = Timestamp(self, timestamp_text)
        self.cue_label = CueLabel(self, cue_label_text)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.timestamp, 1)
        self.layout.addWidget(self.cue_label, 6)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._apply_styles()

    def _apply_styles(self):
        self.setObjectName("cue_box")
        self.setStyleSheet("#cue_box {border-top: 1px solid black;}")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def resize_cue_box(self):
        beat_frame = (
            self.cue_frame.cue_scroll.act_sheet.splitter.beat_scroll.act_beat_frame
        )
        height = beat_frame.beat_size + beat_frame.steps_label_height
        self.setFixedHeight(height)

        self.timestamp.resize_timestamp()
        self.cue_label.resize_cue_label()
