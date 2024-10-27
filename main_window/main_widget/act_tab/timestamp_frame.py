from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.act_tab.lyric_label import LyricLabel
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
        self.lyric_labels: dict[int, LyricLabel] = {}
        self.info_containers: dict[int, QFrame] = {}

        self.setup_layout()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def setup_layout(self):
        """Initializes main layout settings for the timestamp frame."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def init_timestamps(self, num_rows: int):
        """Creates and stores timestamp, lyric label, and info container for each row."""
        for row in range(num_rows):
            timestamp = Timestamp(self, f"{row * 10}:00")
            lyric_label = LyricLabel(self, "")
            info_container = self.create_info_container(timestamp, lyric_label)

            self.timestamps[row] = timestamp
            self.lyric_labels[row] = lyric_label
            self.info_containers[row] = info_container

            self.layout.addWidget(info_container)
            timestamp.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def create_info_container(
        self, timestamp: Timestamp, lyric_label: LyricLabel
    ) -> QFrame:
        """Sets up and returns a QFrame containing timestamp and lyric label."""
        info_container = QFrame(self)
        info_container_layout = QVBoxLayout(info_container)

        info_container.setObjectName("info_container")
        info_container.setStyleSheet(" #info_container {border-top: 1px solid black;}")
        info_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        info_container.setContentsMargins(0, 0, 0, 0)

        info_container_layout.addWidget(timestamp, 1)
        info_container_layout.addWidget(lyric_label, 3)

        return info_container

    def resize_timestamp_frame(self):
        """Applies calculated size settings to all elements in the timestamp frame."""
        beat_size = self.act_tab.beat_scroll_area.act_beat_frame.beat_size
        container_width = self.timestamp_scroll_area.width()

        for info_container in self.info_containers.values():
            info_container.setFixedHeight(beat_size)
            info_container.setFixedWidth(container_width)
        for timestamp in self.timestamps.values():
            timestamp.resize_timestamp()
        for lyric_label in self.lyric_labels.values():
            lyric_label.resize_lyric_label()
