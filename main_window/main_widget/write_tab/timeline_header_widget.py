import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from main_window.main_widget.write_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline import Timeline


class TimelineHeaderWidget(QWidget):
    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline)
        self.timeline = timeline
        self.settings_manager = self.timeline.main_widget.main_window.settings_manager

        # Setup header layout and components
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
        # Create labels for title, date (non-editable), and custom fields
        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Load title from settings
        saved_title = self.settings_manager.write_tab_settings.get_act_title()
        self.title_label = EditableLabel(saved_title, self, font_size=20)
        self.author_label = QLabel(self)

        self.author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add the labels to the layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(self.date_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.author_label)
        self.setLayout(layout)

        # Set the default date
        self.set_date(datetime.datetime.now().strftime("%m/%d/%Y"))
        self.display_author()

        # Connect the EditableLabel text change to save the title automatically
        self.title_label.edit.returnPressed.connect(self.save_title)

    def set_title(self, text: str):
        """Set the title text programmatically."""
        self.title_label.set_text(text)

    def set_date(self, text: str):
        """Set the date text programmatically for the QLabel."""
        self.date_label.setText(text)

    def display_author(self):
        author = (
            self.timeline.main_widget.main_window.settings_manager.users.user_manager.get_current_user()
        )
        self.author_label.setText(f"Choreography by {author}")

    def save_title(self):
        """Save the title to settings when it's changed."""
        new_title = self.title_label.get_text()
        self.settings_manager.write_tab_settings.save_act_title(new_title)

    def resize_header_widget(self):
        """Resize the title label based on the timeline width."""
        self.title_size = self.timeline.width() // 35
        title_label_stylesheet = (
            f"font-size: {self.title_size}px; "
            f"font-weight: bold; "
            f"font-family: 'Monotype Corsiva', cursive;"
        )
        self.title_label.label.setStyleSheet(title_label_stylesheet)

        date_label_stylesheet = f"font-size: {self.title_size // 3}px;"
        self.date_label.setStyleSheet(date_label_stylesheet)
        self.author_label.setStyleSheet(date_label_stylesheet)
