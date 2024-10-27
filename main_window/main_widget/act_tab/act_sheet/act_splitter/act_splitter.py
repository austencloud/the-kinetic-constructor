from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSplitter, QScrollArea
from PyQt6.QtCore import Qt

from .cue_scroll.cue_scroll import CueScroll
from .act_beat_scroll.act_beat_scroll import ActBeatScrollArea

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_sheet import ActSheet
    from main_window.main_widget.main_widget import MainWidget


class ActSplitter(QSplitter):
    def __init__(self, act_sheet: "ActSheet") -> None:
        super().__init__(Qt.Orientation.Horizontal, act_sheet)
        self.act_sheet = act_sheet
        self.main_widget = act_sheet.main_widget

        # Initialize scroll areas
        self.cue_scroll = CueScroll(self.act_sheet)
        self.beat_scroll_area = ActBeatScrollArea(self.act_sheet)

        # Add widgets to the splitter
        self.addWidget(self.cue_scroll)
        self.addWidget(self.beat_scroll_area)

        # Configure splitter appearance and behavior
        self.setHandleWidth(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("margin: 0px; padding: 0px; spacing: 0px;")
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 10)
        self.splitterMoved.connect(self.on_splitter_moved)

    def on_splitter_moved(self, pos, index):
        self.save_splitter_state()
        self.cue_scroll.timestamp_frame.resize_timestamp_frame()
        self.beat_scroll_area.act_beat_frame.resize_act_beat_frame()

    def save_splitter_state(self):
        settings = self.main_widget.settings_manager.settings
        settings.setValue("act_sheet/splitter_state", self.saveState())

    def restore_splitter_state(self):
        settings = self.main_widget.settings_manager.settings
        splitter_state = settings.value("act_sheet/splitter_state")
        if splitter_state:
            self.restoreState(splitter_state)

    def save_scrollbar_state(self):
        settings = self.main_widget.settings_manager.settings
        settings.setValue("act_sheet/scrollbar_state", self.sender().value())

    def restore_scrollbar_state(self):
        settings = self.main_widget.settings_manager.settings
        beat_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if beat_scrollbar_state:
            self.beat_scroll_area.verticalScrollBar().setValue(
                int(beat_scrollbar_state)
            )
        timestamp_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if timestamp_scrollbar_state:
            self.cue_scroll.verticalScrollBar().setValue(int(timestamp_scrollbar_state))

    def connect_scroll_sync(self):
        """Synchronize the scrollbars of the timestamp and beat scroll areas."""
        scroll_areas: list[tuple[QScrollArea, QScrollArea]] = [
            (self.beat_scroll_area, self.cue_scroll),
            (self.cue_scroll, self.beat_scroll_area),
        ]

        for source, target in scroll_areas:
            source.verticalScrollBar().valueChanged.connect(
                target.verticalScrollBar().setValue
            )
            source.verticalScrollBar().valueChanged.connect(self.save_scrollbar_state)
