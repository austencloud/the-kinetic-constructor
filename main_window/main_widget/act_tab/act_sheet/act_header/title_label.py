from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRect
from ....act_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from .act_header import ActHeader


class TitleLabel(EditableLabel):
    def __init__(self, header_widget: "ActHeader", title_text: str):
        super().__init__(header_widget, title_text)
        self.header_widget = header_widget
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set background color and padding for the edit box
        self.edit.setStyleSheet("background-color: #F0F0F0; padding: 5px;")

        # Connect textChanged signal to dynamically adjust size and keep centered
        self.edit.textChanged.connect(self._adjust_edit_geometry)

    def _show_edit(self, event=None):
        """Show the QLineEdit for editing with the current title pre-filled."""
        # Lock the edit height to prevent layout shifting
        self.edit.setFixedHeight(self.label.height())
        
        # Call the superclass method to maintain EditableLabelManager functionality
        super()._show_edit(event)

        # Set initial geometry and center
        self._adjust_edit_geometry()

    def _hide_edit(self):
        """Save changes and hide the editor."""
        # Unlock the height to restore flexibility
        self.edit.setFixedHeight(0)
        
        # Call the superclass method to maintain EditableLabelManager functionality
        super()._hide_edit()

    def _adjust_edit_geometry(self):
        """Adjust geometry to keep the QLineEdit centered based on text content."""
        # Calculate width based on text length
        text_width = self.edit.fontMetrics().horizontalAdvance(self.edit.text()) + 20

        # Get the label's center point
        label_rect = self.label.geometry()
        center_x = label_rect.center().x()

        # Center the edit field around the label’s center
        edit_x = center_x - (text_width // 2)
        self.edit.setGeometry(
            QRect(edit_x, label_rect.y(), text_width, label_rect.height())
        )

    def resize_title_label(self):
        """Resize the title label based on the act sheet width."""
        title_size = self.header_widget.act_sheet.width() // 20
        title_label_stylesheet = (
            f"font-size: {title_size}px; "
            f"font-weight: bold; "
            f"font-family: 'Monotype Corsiva', cursive;"
        )
        self.label.setStyleSheet(title_label_stylesheet)

        # Synchronize edit field size with label size
        self._adjust_edit_geometry()  # Recenter after resizing
