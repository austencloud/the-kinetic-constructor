# timeline_header_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.editable_label import EditableLabel

class TimelineHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setup header layout and components
        self.setObjectName("timelineHeader")
        self.setStyleSheet("""
            #timelineHeader {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid black;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        self._setup_header()

    def _setup_header(self):
        # Create editable labels for title, date, and custom fields
        self.date_label = EditableLabel("Date:", self)
        self.title_label = EditableLabel("Title:", self, font_size=20)  # Larger font size for the title
        self.custom_label = EditableLabel("Custom Label", self)

        # Add the labels to the layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.date_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.custom_label)
        self.setLayout(layout)

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
