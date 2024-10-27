from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame
from PyQt6.QtCore import Qt
from .cue_frame.cue_frame import CueFrame

if TYPE_CHECKING:
    from ...act_sheet import ActSheet


class CueScroll(QScrollArea):
    def __init__(self, act_sheet: "ActSheet"):
        super().__init__(act_sheet)
        self.act_sheet = act_sheet
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self.cue_frame = CueFrame(self)
        self.cue_frame.init_cue_boxes(num_rows=20)
        self.setWidget(self.cue_frame)
        self.setStyleSheet("background: transparent; padding: 0px; margin: 0px;")

    def resize_cue_scroll(self):
        self.cue_frame.resize_cue_frame()
