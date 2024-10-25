from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout
from main_window.main_widget.write_tab.timeline_header_widget import (
    TimelineHeaderWidget,
)
from .timeline import Timeline
from ..act_browser import ActBrowser

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget

from .act_beat_frame import ActBeatFrame


class WriteTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.header_widget = TimelineHeaderWidget(self)

        # Wrap the beat frame inside a QScrollArea
        self.beat_scroll_area = QScrollArea(self)
        self.beat_scroll_area.setWidgetResizable(True)
        self.beat_scroll_area.setStyleSheet(
            "QScrollArea { background-color: transparent; }"
        )
        self.beat_frame = ActBeatFrame(self)
        self.beat_frame.init_act(num_beats=8, num_rows=10)  # Number of beats and rows
        self.beat_scroll_area.setWidget(
            self.beat_frame
        )  # Set ActBeatFrame as the scrollable content

        self.act_browser = ActBrowser(self)

    def _setup_layout(self):
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.act_browser)  # Add the ActBrowser

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.header_widget)
        self.left_layout.addWidget(self.beat_scroll_area)  # Add scroll area for beats

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addLayout(self.left_layout, 1)
        self.layout.addLayout(self.right_layout, 1)
        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.header_widget.resize_header_widget()
        self.beat_frame.resizeEvent(event)  # Make sure the beat frame resizes correctly
        self.act_browser.resize_browser()

    def on_splitter_moved(self):
        self.beat_frame.resizeEvent(None)
        self.act_browser.resize_browser()
