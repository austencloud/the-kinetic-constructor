from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, QSettings

from main_window.main_widget.act_browser import ActBrowser

from .timestamp_scroll_area import TimestampScrollArea
from .act_beat_scroll_area import ActBeatScrollArea
from .splitter_manager import SplitterManager
from main_window.main_widget.write_tab.act_header_widget import ActHeaderWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ActTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.header_widget = ActHeaderWidget(self)
        self.timestamp_scroll_area = TimestampScrollArea(self)
        self.beat_scroll_area = ActBeatScrollArea(self)
        self.splitter_manager = SplitterManager(self)
        self.act_browser = ActBrowser(self)

        self._setup_layout()
        self._connect_scrolls()

    def _connect_scrolls(self):
        self.beat_scroll_area.verticalScrollBar().valueChanged.connect(
            self.timestamp_scroll_area.verticalScrollBar().setValue
        )
        self.timestamp_scroll_area.verticalScrollBar().valueChanged.connect(
            self.beat_scroll_area.verticalScrollBar().setValue
        )

    def _setup_layout(self):
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.header_widget, 1)
        self.left_layout.addWidget(self.splitter_manager.splitter, 10)
        self.left_layout.setSpacing(0)
        self.left_layout.setContentsMargins(0, 0, 0, 0)

        self.right_layout = QVBoxLayout()
        self.right_layout.setSpacing(0)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.addWidget(self.act_browser)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 1)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.header_widget.resize_header_widget()
        self.act_browser.resize_browser()
        self.beat_scroll_area.resize_act_beat_frame()
        self.timestamp_scroll_area.resize_timestamp_frame()

    def closeEvent(self, event):
        self.splitter_manager.save_splitter_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.splitter_manager.restore_splitter_state()
        super().showEvent(event)
