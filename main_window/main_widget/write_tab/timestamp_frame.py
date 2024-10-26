from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.timestamp import Timestamp

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class TimestampFrame(QWidget):
    def __init__(self, write_tab: "WriteTab"):
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.timestamps: dict[int, Timestamp] = {}
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # set transparent background
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

    def init_timestamps(self, num_rows):
        for row in range(num_rows):
            timestamp = Timestamp(self, f"{row * 10}:00")  # Example: 0:00, 0:10, etc.
            self.timestamps.update({row: timestamp})
            self.layout.addWidget(timestamp)
            timestamp.setVisible(True)
            timestamp.label.setAlignment(Qt.AlignmentFlag.AlignTop)
            timestamp.label.setVisible(True)

    def resize_timestamp_frame(self):
        for timestamp in self.timestamps.values():
            timestamp.resize_timestamp()
