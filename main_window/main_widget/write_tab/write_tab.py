from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QFrame, QSplitter
from main_window.main_widget.write_tab.act_header_widget import (
    ActHeaderWidget,
)
from PyQt6.QtCore import Qt, QSettings
from main_window.main_widget.write_tab.timestamp_frame import TimestampFrame
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
        self.header_widget = ActHeaderWidget(self)

        # Create the timestamp scroll area
        self.timestamp_scroll_area = QScrollArea(self)
        self.timestamp_scroll_area.setWidgetResizable(True)
        self.timestamp_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.timestamp_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.timestamp_scroll_area.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground, True
        )
        self.timestamp_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.timestamp_scroll_area.setViewportMargins(0, 0, 0, 0)

        self.timestamp_frame = TimestampFrame(self)
        self.timestamp_frame.init_timestamps(num_rows=20)
        self.timestamp_scroll_area.setWidget(self.timestamp_frame)
        self.timestamp_scroll_area.setContentsMargins(0, 0, 0, 0)

        # Create the beat grid scroll area
        self.beat_scroll_area = QScrollArea(self)
        self.beat_scroll_area.setWidgetResizable(True)
        self.beat_scroll_area.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.beat_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.beat_scroll_area.setViewportMargins(0, 0, 0, 0)

        self.act_beat_frame = ActBeatFrame(self)
        self.act_beat_frame.init_act(num_beats=8, num_rows=10)
        self.beat_scroll_area.setWidget(self.act_beat_frame)

        # Synchronize vertical scrolling
        self.timestamp_scroll_area.verticalScrollBar().valueChanged.connect(
            self.beat_scroll_area.verticalScrollBar().setValue
        )
        self.beat_scroll_area.verticalScrollBar().valueChanged.connect(
            self.timestamp_scroll_area.verticalScrollBar().setValue
        )

        # Create a QSplitter for the timestamps and beats
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.timestamp_scroll_area)
        self.splitter.addWidget(self.beat_scroll_area)

        # Set initial sizes for the splitter widgets
        self.splitter.setSizes([100, 800])  # Adjust these values as needed

        # Optionally, set the handle width
        self.splitter.setHandleWidth(5)

        self.act_browser = ActBrowser(self)

    def _setup_layout(self):
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.header_widget)
        self.left_layout.addWidget(self.splitter)
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
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.header_widget.resize_header_widget()
        self.act_browser.resize_browser()
        self.act_beat_frame.resize_act_beat_frame()
        self.timestamp_frame.resize_timestamp_frame()

    # Optionally, save and restore splitter state
    def closeEvent(self, event):
        settings = QSettings('YourCompany', 'YourApp')
        settings.setValue('write_tab_splitter_state', self.splitter.saveState())
        super().closeEvent(event)

    def showEvent(self, event):
        settings = QSettings('YourCompany', 'YourApp')
        splitter_state = settings.value('write_tab_splitter_state')
        if splitter_state:
            self.splitter.restoreState(splitter_state)
        super().showEvent(event)
