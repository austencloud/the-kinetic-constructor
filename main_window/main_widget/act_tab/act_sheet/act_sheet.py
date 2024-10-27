from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .act_header.act_header import ActHeader
from .act_splitter.act_splitter import ActSplitter

if TYPE_CHECKING:
    from ..act_tab import ActTab


class ActSheet(QWidget):
    def __init__(self, act_tab: "ActTab") -> None:
        super().__init__(act_tab)
        self.act_tab = act_tab
        self.main_widget = act_tab.main_widget

        self.header = ActHeader(self)
        self.splitter = ActSplitter(self)

        self._setup_layout()
        self.splitter.connect_scroll_sync() 

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
        self.splitter.beat_scroll_area.act_beat_frame.resize_act_beat_frame()
        self.splitter.timestamp_scroll_area.resize_timestamp_frame()

    def closeEvent(self, event):
        self.splitter.save_splitter_state()
        self.splitter.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.splitter.restore_splitter_state()
        self.splitter.restore_scrollbar_state()
        super().showEvent(event)
