from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSplitter
from PyQt6.QtCore import Qt, QSettings


if TYPE_CHECKING:
    from main_window.main_widget.write_tab.act_tab import ActTab
    from main_window.main_widget.write_tab.act_beat_scroll_area import ActBeatScrollArea
    from main_window.main_widget.write_tab.timestamp_scroll_area import (
        TimestampScrollArea,
    )


class SplitterManager:
    def __init__(self, act_tab: "ActTab"):

        self.timestamp_scroll_area: "TimestampScrollArea" = (
            act_tab.timestamp_scroll_area
        )
        self.act_beat_scroll_area: "ActBeatScrollArea" = act_tab.beat_scroll_area
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.splitter.addWidget(self.timestamp_scroll_area)
        self.splitter.addWidget(self.act_beat_scroll_area)

        self.splitter.splitterMoved.connect(self.on_splitter_moved)

        self.timestamp_scroll_area = self.timestamp_scroll_area
        self.beat_scroll_area = self.act_beat_scroll_area

    def on_splitter_moved(self, pos, index):
        self.timestamp_scroll_area.resize_timestamp_frame()
        self.beat_scroll_area.resize_act_beat_frame()

    def save_splitter_state(self):
        settings = QSettings("YourCompany", "YourApp")
        settings.setValue("write_tab_splitter_state", self.splitter.saveState())

    def restore_splitter_state(self):
        settings = QSettings("YourCompany", "YourApp")
        splitter_state = settings.value("write_tab_splitter_state")
        if splitter_state:
            self.splitter.restoreState(splitter_state)
