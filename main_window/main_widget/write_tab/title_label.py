# timestamp_label.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

from main_window.main_widget.write_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.write_tab.timeline_header_widget import (
        TimelineHeaderWidget,
    )


class TitleLabel(EditableLabel):
    def __init__(self, title_text, header_widget: "TimelineHeaderWidget"):
        super().__init__(title_text, header_widget)
        self.header_widget = header_widget

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current timestamp pre-filled."""
        self.edit.setText(self.label.text())  # Pre-fill with current timestamp
        current_font = self.label.font()
        self.edit.setFont(current_font)
        self.label.setVisible(False)
        self.edit.setVisible(True)
        self.edit.setFocus()
        self.edit.selectAll()
        self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Ensure that the timestamp format is preserved during editing

    def _hide_edit(self):
        """Ensure timestamp format on hiding the editor."""
        new_text = self.edit.text()

        self.label.setText(new_text if new_text else self.label.text())
        self.label.setVisible(True)
        self.edit.setVisible(False)

    def set_text(self, text: str):
        """Set the text ensuring it's formatted as a timestamp."""
        # You can add logic to format the timestamp here if needed
        self.label.setText(text)

    def resize_title_label(self):
        """Resize the title label based on the timeline width."""
        self.title_size = self.header_widget.write_tab.width() // 50
        title_label_stylesheet = (
            f"font-size: {self.title_size}px; "
            f"font-weight: bold; "
            f"font-family: 'Monotype Corsiva', cursive;"
        )
        self.label.setStyleSheet(title_label_stylesheet)
