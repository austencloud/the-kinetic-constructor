# timeline_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QPalette, QColor

from main_window.main_widget.write_tab.act_header_widget import (
    ActHeaderWidget,
)
from main_window.main_widget.write_tab.timeline_scroll_area import TimelineScrollArea
from .timeline_row import TimelineRow

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


class Timeline(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.main_widget = write_tab.main_widget
        self.rows: list[TimelineRow] = []

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.header_widget = ActHeaderWidget(self)
        self.scroll_area = TimelineScrollArea(self)
        self.scroll_area.add_default_rows(8)  # Example: 8 default rows

    def setup_rows(self):
        """Setup rows after the main_widget is ready."""
        for row in self.rows:
            row.setup_beats(self.main_widget)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.header_widget)  # Add header at the top
        self.layout.addWidget(self.scroll_area)  # Add scroll area for rows below
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

    def resize_timeline(self):
        self.header_widget.resize_header_widget()
        self.scroll_area.resize_timeline_scroll_area()
