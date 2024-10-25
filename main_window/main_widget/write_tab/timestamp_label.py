# timestamp_label.py
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

from main_window.main_widget.write_tab.editable_label import EditableLabel


class TimestampLabel(EditableLabel):
    def __init__(self, label_text="0:00", parent=None, font_size: int = 14):
        super().__init__(label_text, parent)

    def _show_edit(self, event):
        """Show the QLineEdit for editing with the current timestamp pre-filled."""
        self.edit.setText(self.label.text())  # Pre-fill with current timestamp
        self.label.setVisible(False)
        self.edit.setVisible(True)
        self.edit.setFocus()
        self.edit.selectAll()
        self.edit.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Ensure that the timestamp format is preserved during editing

    def _hide_edit(self):
        """Ensure timestamp format on hiding the editor."""
        new_text = self.edit.text()

        # Add any additional checks here if needed to enforce timestamp formatting
        # (like if you want it always in the format mm:ss)

        self.label.setText(new_text if new_text else self.label.text())
        self.label.setVisible(True)
        self.edit.setVisible(False)

    def set_text(self, text: str):
        """Set the text ensuring it's formatted as a timestamp."""
        # You can add logic to format the timestamp here if needed
        self.label.setText(text)

    def resize_timestamp(self, parent_width: int):
        """Resize the font size based on parent width."""
        font_size = int(parent_width / 80)  # Adjust the divisor for size proportions
        font = self.label.font()
        font.setPointSize(font_size)
        self.label.setFont(font)
        self.edit.setFont(font)
