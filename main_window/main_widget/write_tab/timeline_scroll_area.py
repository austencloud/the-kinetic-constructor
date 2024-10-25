from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
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
        row_number = len(self.rows) + 1
        row = TimelineRow(self)  # Pass row number for beat numbers
        self.content_layout.addWidget(row)
        row.setup_beats()  # Call setup_beats after adding the row
        self.rows[len(self.rows)] = row

    def resize_timeline_scroll_area(self):
        for row in self.rows.values():
            row.resize_row()

    def resizeEvent(self, event):
        self.resize_timeline_scroll_area()
        super().resizeEvent(event)
