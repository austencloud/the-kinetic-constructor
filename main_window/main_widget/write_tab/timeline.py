# timeline_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.write_tab.timeline_header_widget import (
    TimelineHeaderWidget,
)
from main_window.main_widget.write_tab.timeline_scroll_area import TimelineScrollArea
from .timeline_row import TimelineRow

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


# timeline_widget.py
class Timeline(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.rows: list[TimelineRow] = []

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        # Create the scroll area for rows
        self.scroll_area = TimelineScrollArea(self)
        # Add default rows to the scroll area
        self.scroll_area.add_default_rows(8)  # Example: 8 default rows

    def setup_rows(self, main_widget):
        """Setup rows after the main_widget is ready."""
        for row in self.rows:
            row.setup_beats(main_widget)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resize_timeline(self):
        self.scroll_area.resize_timeline()
