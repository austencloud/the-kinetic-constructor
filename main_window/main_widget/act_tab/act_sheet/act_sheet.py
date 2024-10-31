from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .act_header.act_header import ActHeader
from .act_splitter.act_frame import ActFrame

if TYPE_CHECKING:
    from ..act_tab import ActTab


class ActSheet(QWidget):
    DEFAULT_ROWS = 24
    DEFAULT_COLUMNS = 8

    def __init__(self, act_tab: "ActTab") -> None:
        super().__init__(act_tab)
        self.act_tab = act_tab
        self.main_widget = act_tab.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager.act_sheet
        self.act_header = ActHeader(self)
        self.act_frame = ActFrame(self)
        self.setAcceptDrops(False)

        self._setup_layout()
        self.act_frame.connect_scroll_sync()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.act_header, 1)
        layout.addWidget(self.act_frame, 10)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resize_act_sheet(self):
        """Resize each part when ActSheet resizes."""
        self.act_header.resize_header_widget()
        self.act_frame.beat_scroll.act_beat_frame.resize_act_beat_frame()
        self.act_frame.cue_scroll.resize_cue_scroll()

    def closeEvent(self, event):
        self.act_frame.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.act_frame.restore_scrollbar_state()
        super().showEvent(event)
