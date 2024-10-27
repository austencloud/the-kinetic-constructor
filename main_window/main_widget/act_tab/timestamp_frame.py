from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.act_tab.lyric_label import LyricLabel
from main_window.main_widget.act_tab.timestamp import Timestamp

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.timestamp_scroll_area import TimestampScrollArea
    from main_window.main_widget.act_tab.act_tab import ActTab


class TimestampFrame(QWidget):
    def __init__(self, timestamp_scroll_area: "TimestampScrollArea"):
        super().__init__(timestamp_scroll_area)
        self.act_tab = timestamp_scroll_area.act_sheet
        self.timestamp_scroll_area = timestamp_scroll_area
        self.timestamps: dict[int, Timestamp] = {}
        self.lyric_labels: dict[int, LyricLabel] = {}
        self.info_containers: dict[int, QFrame] = {}
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def init_timestamps(self, num_rows):
        for row in range(num_rows):
            timestamp = Timestamp(self, f"{row * 10}:00")
            lyric_label = LyricLabel(self, "")
            info_container = QFrame(self)
            info_container_layout = QVBoxLayout(info_container)
            
            # Apply Expanding policy to info_container
            info_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            info_container.setContentsMargins(0, 0, 0, 0)
            info_container.setObjectName("info_container")
            info_container.setStyleSheet(
                """
                #info_container {
                    border-top: 1px solid black;
                }
                """
            )
            
            # Store components
            self.timestamps[row] = timestamp
            self.lyric_labels[row] = lyric_label
            self.info_containers[row] = info_container
            
            # Add widgets with fixed ratios in the layout
            info_container_layout.addWidget(timestamp, 1)
            info_container_layout.addWidget(lyric_label, 3)
            self.layout.addWidget(info_container)

            timestamp.label.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def resize_timestamp_frame(self):
        # Calculate the height of each beat and set it to info_containers
        width_without_scrollbar = (
            self.act_tab.beat_scroll_area.act_beat_frame.width()
            - self.act_tab.beat_scroll_area.verticalScrollBar().width()
        )
        beat_size = int(width_without_scrollbar // 8)

        # Apply beat size to each info_container, timestamp, and lyric_label
        for info_container in self.info_containers.values():
            info_container.setFixedHeight(beat_size)
            info_container.setFixedWidth(self.timestamp_scroll_area.width())
        for timestamp in self.timestamps.values():
            timestamp.resize_timestamp()
        for lyric_label in self.lyric_labels.values():
            lyric_label.resize_timestamp()
