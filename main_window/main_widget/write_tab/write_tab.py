# write_tab.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QHBoxLayout
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
        self.beat_frame = ActBeatFrame(self)
        self.beat_frame.init_act(num_beats=8, num_rows=10)

        self.timeline = Timeline(self)
        self.act_browser = ActBrowser(self)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.timeline, 1)
        self.layout.addWidget(self.act_browser, 1)
        self.setLayout(self.layout)

        self.setStyleSheet("background-color: rgba(255, 255, 255, 140);")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.timeline.resize_timeline()
        self.act_browser.resize_browser()

    def on_splitter_moved(self):
        self.timeline.resize_timeline()
        self.act_browser.resize_browser()

    # connect the splitter to the resize function
    def load_most_recent_act(self):
        """Load the most recent act and apply its settings."""
        last_act = self.settings_manager.write_tab_settings.load_last_act()
        if last_act:
            pass
