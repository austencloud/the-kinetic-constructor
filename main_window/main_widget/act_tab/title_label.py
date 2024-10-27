from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt, QRect
from main_window.main_widget.act_tab.editable_label import EditableLabel

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_header import ActHeader


# TitleLabel class with custom geometry adjustments
class TitleLabel(EditableLabel):
    def __init__(self, header_widget, title_text):
        super().__init__(
            header_widget,
            title_text,
            align=Qt.AlignmentFlag.AlignCenter,
            bg_color="#F0F0F0",
        )
        self.header_widget: "ActHeader" = header_widget

    def _show_edit(self, event=None):
        super()._show_edit(event)
        self.adjust_edit_geometry()  # Center the edit geometry

    def adjust_edit_geometry(self):
        """Center-aligns edit box based on text width."""
        text_width = self.edit.fontMetrics().horizontalAdvance(self.edit.text()) + 20
        center_x = self.label.geometry().center().x()
        edit_x = center_x - (text_width // 2)
        self.edit.setGeometry(
            QRect(
                edit_x,
                self.label.geometry().y(),
                text_width,
                self.label.geometry().height(),
            )
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
        self.adjust_edit_geometry()  # Recenter after resizing
