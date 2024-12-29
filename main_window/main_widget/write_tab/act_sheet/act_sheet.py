from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.write_tab.act_sheet.act_loader import ActLoader
from .act_header.act_header import ActHeader
from .act_splitter.act_container import ActContainer
from .act_saver import ActSaver
from .sequence_collector import SequenceCollector

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class ActSheet(QWidget):
    DEFAULT_ROWS = 24
    DEFAULT_COLUMNS = 8

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.settings_manager = (
            self.main_widget.main_window.settings_manager.write_tab_settings
        )
        self.act_header = ActHeader(self)
        self.act_container = ActContainer(self)
        self.setAcceptDrops(False)

        self.act_saver = ActSaver(self)
        self.act_loader = ActLoader(self)
        self.sequence_collector = SequenceCollector(self)

        self._setup_layout()
        self.act_container.connect_scroll_sync()

    def populate_from_act_data(self, act_data: dict):
        """Populate ActSheet from saved JSON data."""

        self.act_header.set_title(act_data.get("title", "Untitled Act"))
        self.main_widget.manager.set_grid_mode(act_data.get("grid_mode", "diamond"))

        for sequence in act_data["sequences"]:
            self.act_container.beat_scroll.act_beat_frame.populator.populate_beats(
                sequence
            )

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.act_header, 1)
        layout.addWidget(self.act_container, 10)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def closeEvent(self, event):
        self.act_container.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.act_container.restore_scrollbar_state()
        super().showEvent(event)
