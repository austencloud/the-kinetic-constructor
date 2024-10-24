# timeline_widget.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.write_widget.timeline_scroll_area import TimelineScrollArea
from .timeline_row import TimelineRow

if TYPE_CHECKING:
    from main_window.main_widget.write_widget.write_widget import WriteWidget


class Timeline(QWidget):
    def __init__(self, write_tab: "WriteWidget") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.rows: list[TimelineRow] = []

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        # Use the custom scroll area
        self.scroll_area = TimelineScrollArea(self)
        # Add the content widget to the custom scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)

        # Add default rows
        self.add_default_rows(8)  # For example, setting 8 default rows

    def add_default_rows(self, number_of_rows):
        for _ in range(number_of_rows):
            self.add_row()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def add_row(self):
        row = TimelineRow(self)
        self.rows.append(row)
        self.content_layout.addWidget(row)

    def resize_timeline(self):
        for row in self.rows:
            row.resize_row()
