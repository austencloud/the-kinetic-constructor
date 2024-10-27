from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, QSettings

from .timestamp_scroll_area import TimestampScrollArea
from .act_beat_scroll_area import ActBeatScrollArea
from main_window.main_widget.act_tab.act_header_widget import ActHeader

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ActSheet(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.initialized = False
        # Instantiate widgets
        self.header = ActHeader(self)
        self.timestamp_scroll_area = TimestampScrollArea(self)
        self.beat_scroll_area = ActBeatScrollArea(self)

        # Configure splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.timestamp_scroll_area)
        self.splitter.addWidget(self.beat_scroll_area)

        # Remove handle space, set stretch, and zero margins
        self.splitter.setHandleWidth(0)
        self.splitter.setContentsMargins(0, 0, 0, 0)
        self.splitter.setStyleSheet("margin: 0px; padding: 0px; spacing: 0px;")
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 10)
        self.splitter.splitterMoved.connect(self.on_splitter_moved)
        self._setup_layout()
        self._connect_scrolls()

    def on_splitter_moved(self, pos, index):
        self.save_splitter_state()
        self.timestamp_scroll_area.timestamp_frame.resize_timestamp_frame()
        self.beat_scroll_area.act_beat_frame.resize_act_beat_frame()

    def save_splitter_state(self):
        settings = self.main_widget.settings_manager.settings
        settings.setValue("act_sheet/splitter_state", self.splitter.saveState())

    def restore_splitter_state(self):
        settings = self.main_widget.settings_manager.settings
        splitter_state = settings.value("act_sheet/splitter_state")
        if splitter_state:
            self.splitter.restoreState(splitter_state)

    def restore_scrollbar_state(self):
        settings = self.main_widget.settings_manager.settings
        beat_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if beat_scrollbar_state:
            self.beat_scroll_area.verticalScrollBar().setValue(
                int(beat_scrollbar_state)
            )
        timestamp_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if timestamp_scrollbar_state:
            self.timestamp_scroll_area.verticalScrollBar().setValue(
                int(timestamp_scrollbar_state)
            )

    def _connect_scrolls(self):
        self.beat_scroll_area.verticalScrollBar().valueChanged.connect(
            self.timestamp_scroll_area.verticalScrollBar().setValue
        )
        self.timestamp_scroll_area.verticalScrollBar().valueChanged.connect(
            self.beat_scroll_area.verticalScrollBar().setValue
        )
        self.beat_scroll_area.verticalScrollBar().valueChanged.connect(
            self.save_scrollbar_state  # Save splitter state when scrolling
        )
        self.timestamp_scroll_area.verticalScrollBar().valueChanged.connect(
            self.save_scrollbar_state  # Save splitter state when scrolling
        )

    def save_scrollbar_state(self):
        settings = self.main_widget.settings_manager.settings
        settings.setValue("act_sheet/scrollbar_state", self.sender().value())

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.header, 1)
        layout.addWidget(self.splitter, 10)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resize_act_sheet(self):
        """Resize each part when ActSheet resizes."""
        self.header.resize_header_widget()
        self.beat_scroll_area.act_beat_frame.resize_act_beat_frame()
        self.timestamp_scroll_area.resize_timestamp_frame()

    def closeEvent(self, event):
        self.save_splitter_state()
        self.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.restore_splitter_state()
        self.restore_scrollbar_state()
        super().showEvent(event)
