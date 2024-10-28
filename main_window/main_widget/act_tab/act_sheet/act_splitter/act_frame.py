from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QFrame, QHBoxLayout
from .act_beat_scroll.act_beat_scroll import ActBeatScroll
from .cue_scroll.cue_scroll import CueScroll

if TYPE_CHECKING:
    from ..act_sheet import ActSheet


class ActFrame(QFrame):
    def __init__(self, act_sheet: "ActSheet") -> None:
        super().__init__(act_sheet)
        self.act_sheet = act_sheet
        self.main_widget = act_sheet.main_widget

        # Initialize scroll areas
        self.cue_scroll = CueScroll(self.act_sheet)
        self.beat_scroll = ActBeatScroll(self.act_sheet)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        # Add widgets to the splitter
        self.layout.addWidget(self.cue_scroll, 1)
        self.layout.addWidget(self.beat_scroll, 8)

        # Configure splitter appearance and behavior
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("margin: 0px; padding: 0px; spacing: 0px;")

    def on_splitter_moved(self, pos, index):
        self.save_splitter_state()
        self.cue_scroll.cue_frame.resize_cue_frame()
        self.beat_scroll.act_beat_frame.resize_act_beat_frame()

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
            self.beat_scroll.verticalScrollBar().setValue(int(beat_scrollbar_state))
        timestamp_scrollbar_state = settings.value("act_sheet/scrollbar_state")
        if timestamp_scrollbar_state:
            self.cue_scroll.verticalScrollBar().setValue(int(timestamp_scrollbar_state))

    def connect_scroll_sync(self):
        """Synchronize the scrollbars of the timestamp and beat scroll areas."""
        scroll_areas: list[tuple[QScrollArea, QScrollArea]] = [
            (self.beat_scroll, self.cue_scroll),
            (self.cue_scroll, self.beat_scroll),
        ]

        for source, target in scroll_areas:
            source.verticalScrollBar().valueChanged.connect(
                target.verticalScrollBar().setValue
            )
            source.verticalScrollBar().valueChanged.connect(self.save_scrollbar_state)
