from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from main_window.main_widget.act_tab.timestamp import Timestamp

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.timestamp_scroll_area import (
        TimestampScrollArea,
    )
    from main_window.main_widget.act_tab.act_tab import ActTab


class TimestampFrame(QWidget):
    def __init__(self, timestamp_scroll_area: "TimestampScrollArea"):
        super().__init__(timestamp_scroll_area)
        self.act_tab = timestamp_scroll_area.act_sheet
        self.timestamp_scroll_area = timestamp_scroll_area
        self.timestamps: dict[int, Timestamp] = {}
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def init_timestamps(self, num_rows):
        for row in range(num_rows):
            timestamp = Timestamp(self, f"{row * 10}:00")  # Example: 0:00, 0:10, etc.
            self.timestamps.update({row: timestamp})
            self.layout.addWidget(timestamp)
            timestamp.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def resize_timestamp_frame(self):
        for timestamp in self.timestamps.values():
            timestamp.resize_timestamp()
