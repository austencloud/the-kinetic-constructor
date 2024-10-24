# custom_scroll_area.py
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

from main_window.main_widget.write_widget.editable_label import EditableLabel


class TimelineScrollArea(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)

        # Create a content widget for the scroll area
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_widget.setLayout(self.content_layout)

        self.setWidget(self.content_widget)

        # Set translucent background color
        self.set_translucent_background()

        # Add header (title, date, custom labels)
        self._setup_header()

    def _setup_header(self):
        # Create editable labels for title and date
        self.title_label = EditableLabel("Title:", self)
        self.date_label = EditableLabel("Date:", self)

        # Add custom labels or other fields as needed
        self.custom_label = EditableLabel("Custom Label", self)

        # Create a header widget and layout
        self.header_widget = QWidget()
        self.header_layout = QVBoxLayout(self.header_widget)
        self.header_widget.setLayout(self.header_layout)

        # Add title, date, and custom labels to the header layout
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addWidget(self.date_label)
        self.header_layout.addWidget(self.custom_label)

        # Add the header to the scroll area
        self.content_layout.addWidget(self.header_widget)

    def set_translucent_background(self):
        """Set the background of the scroll area to a translucent white."""
        p = self.palette()
        p.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255, 128))  # 128 is the alpha for transparency
        self.setPalette(p)
        self.setAutoFillBackground(True)

    def set_title(self, text: str):
        """Programmatically set the title text."""
        self.title_label.set_text(text)

    def set_date(self, text: str):
        """Programmatically set the date text."""
        self.date_label.set_text(text)

    def add_custom_label(self, label_text: str):
        """Add a custom label programmatically."""
        custom_label = EditableLabel(label_text, self)
        self.header_layout.addWidget(custom_label)