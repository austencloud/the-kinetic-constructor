from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout
from PyQt6.QtCore import Qt
from .timeline_row import TimelineRow

if TYPE_CHECKING:
    from .write_widget import WriteWidget


class Timeline(QWidget):
    def __init__(self, write_tab: "WriteWidget") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab
        self.rows: List[TimelineRow] = []

        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.scroll_area.setWidget(self.content_widget)

        self.add_row()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.scroll_area)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.transparent)
        self.setPalette(p)

        self.setLayout(layout)

    def add_row(self):
        row = TimelineRow(self)
        self.rows.append(row)
        self.content_layout.addWidget(row)

    def resize_timeline(self):
        for row in self.rows:
            row.resize_row()
