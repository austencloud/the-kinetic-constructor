from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.act_beat_frame import ActBeatFrame

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_tab import ActTab


class ActBeatScrollArea(QScrollArea):
    def __init__(self, write_tab: "ActTab"):
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.setWidgetResizable(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self.act_beat_frame = ActBeatFrame(self)
        self.act_beat_frame.init_act(num_beats=8, num_rows=10)
        self.setWidget(self.act_beat_frame)
        self.setStyleSheet("background: transparent;")

    def resize_act_beat_frame(self):
        self.act_beat_frame.resize_act_beat_frame()
