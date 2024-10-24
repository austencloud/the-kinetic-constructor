# timeline_widget.py
from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt

from .timeline_row_widget import TimelineRowWidget

if TYPE_CHECKING:
    from .choreography_tab_widget import ChoreographyTabWidget


class TimelineWidget(QWidget):
    def __init__(self, choreography_tab: "ChoreographyTabWidget") -> None:
        super().__init__(choreography_tab)
        self.choreography_tab = choreography_tab
        self.rows: List[TimelineRowWidget] = []

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)

        # Add initial row
        self.add_row()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        self.setLayout(layout)

    def add_row(self):
        row = TimelineRowWidget(self)
        self.rows.append(row)
        self.content_layout.addWidget(row)

    def resize_timeline(self):
        for row in self.rows:
            row.resize_row()
