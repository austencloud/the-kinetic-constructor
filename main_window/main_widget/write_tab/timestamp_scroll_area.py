from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.timestamp_frame import TimestampFrame

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class TimestampScrollArea(QScrollArea):
    def __init__(self, write_tab: "WriteTab"):
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setViewportMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

        self.timestamp_frame = TimestampFrame(self)
        self.timestamp_frame.init_timestamps(num_rows=20)
        self.setWidget(self.timestamp_frame)

    def resize_timestamp_frame(self):
        self.timestamp_frame.resize_timestamp_frame()
