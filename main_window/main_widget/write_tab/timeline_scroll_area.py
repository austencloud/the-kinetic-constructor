# custom_scroll_area.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QFrame
from PyQt6.QtGui import QColor, QPalette
from main_window.main_widget.write_tab.timeline_row import TimelineRow
if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline import Timeline


class TimelineScrollArea(QScrollArea):
    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline)
        self.timeline = timeline
        self.main_widget = timeline.main_widget
        self.initialized = False
        self.setWidgetResizable(True)
        self.rows: dict[int, TimelineRow] = {}
        # Create the content widget and layout for the rows
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(0)
        self.content_widget.setLayout(self.content_layout)

        # Set the content widget inside the scroll area
        self.setWidget(self.content_widget)
        self.set_translucent_background()

    def set_translucent_background(self):
        """Set the background of the scroll area to a translucent white."""
        p = self.palette()
        p.setColor(
            QPalette.ColorRole.Base, QColor(255, 255, 255, 128)
        )  # 128 for transparency
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def add_default_rows(self, number_of_rows):
        """Add a specific number of timeline rows."""
        for _ in range(number_of_rows):
            self.add_row()

    def add_row(self):
        """Add a single row to the scroll area."""
        row = TimelineRow(self)
        self.content_layout.addWidget(row)
        self.rows[len(self.rows)] = row

    def resize_timeline(self):
        for row in self.rows.values():
            row.resize_row()

    def resizeEvent(self, event):
        self.resize_timeline()
        super().resizeEvent(event)
        if not self.initialized:
            self.add_default_rows(8)  # Example: 8 default rows
