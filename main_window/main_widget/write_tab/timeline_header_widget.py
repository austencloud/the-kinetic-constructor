# timeline_header_widget.py
import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline import Timeline


class TimelineHeaderWidget(QWidget):
    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline)
        # Setup header layout and components
        self.timeline = timeline
        self.setObjectName("timelineHeader")
        self.setStyleSheet(
            """
            #timelineHeader {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
        """
        )
        self._setup_header()

    def _setup_header(self):
        # Create editable labels for title, date, and custom fields
        self.date_label = EditableLabel("Date:", self)
        self.title_label = EditableLabel("Title:", self, font_size=20)
        self.custom_label = EditableLabel("Custom Label", self)

        # Add the labels to the layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.date_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.custom_label)
        self.setLayout(layout)

        # Set default text
        self.set_title("My Timeline Title")
        self.set_date(
            # get the date and time and format it like 05/31/2024
            datetime.datetime.now().strftime("%m/%d/%Y")
        )

    def set_title(self, text: str):
        """Set the title text programmatically."""
        self.title_label.set_text(text)

    def set_date(self, text: str):
        """Set the date text programmatically."""
        self.date_label.set_text(text)

    def add_custom_label(self, label_text: str):
        """Add a custom label programmatically."""
        custom_label = EditableLabel(label_text, self)
        self.layout().addWidget(custom_label)

    def resize_header_widget(self):
        """Resize the title label based on the timeline width."""
        self.title_size = self.timeline.width() // 35
        title_label_stylesheet = (
            f"font-size: {self.title_size}px; "
            f"font-weight: bold; "
            f"font-family: 'Monotype Corsiva', cursive;"
        )
        self.title_label.label.setStyleSheet(title_label_stylesheet)
