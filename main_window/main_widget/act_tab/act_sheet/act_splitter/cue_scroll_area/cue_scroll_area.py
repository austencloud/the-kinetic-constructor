from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.act_tab.act_sheet.act_splitter.cue_scroll_area.cue_frame.cue_frame import (
    CueFrame,
)

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_sheet import ActSheet


class CueScrollArea(QScrollArea):
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

        self.timestamp_frame = CueFrame(self)
        self.timestamp_frame.init_timestamps(num_rows=20)
        self.setWidget(self.timestamp_frame)
        self.setStyleSheet("background: transparent; padding: 0px; margin: 0px;")

    def resize_timestamp_frame(self):
        self.timestamp_frame.resize_timestamp_frame()
