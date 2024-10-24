# timeline_header_widget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from main_window.main_widget.write_tab.editable_label import EditableLabel


class TimelineHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Setup header layout and components
        self._setup_header()

    def _setup_header(self):
        # Create editable labels for title, date, and custom fields
        self.title_label = EditableLabel("Title:", self)
        self.date_label = EditableLabel("Date:", self)
        self.custom_label = EditableLabel("Custom Label", self)

        # Add the labels to the layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.title_label)
        layout.addWidget(self.date_label)
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
