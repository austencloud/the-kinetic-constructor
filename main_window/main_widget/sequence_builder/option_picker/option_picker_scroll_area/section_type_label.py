from typing import TYPE_CHECKING
from PyQt6.QtGui import QEnterEvent
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from Enums.Enums import LetterType
from PyQt6.QtCore import pyqtSignal

from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.letter_type_text_painter import (
    LetterTypeTextPainter,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )


class SectionTypeLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section_widget = section_widget
        self.setContentsMargins(0, 0, 0, 0)
        self.set_styled_text(section_widget.letter_type)

    def set_styled_text(self, letter_type: LetterType) -> None:
        # Access the description directly from the letter_type enum
        letter_type_str = letter_type.name
        styled_type_name = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )

        # Set the text to show the first part of the letter type enum followed by the styled type name
        styled_text = f"{letter_type_str[0:4]} {letter_type_str[4]}: {styled_type_name}"
        self.setText(styled_text)

    def get_font_size(self):
        scroll_area = self.section_widget.scroll_area
        manual_builder = scroll_area.manual_builder
        font_size = manual_builder.width() // 45
        return font_size

    def set_label_style(self, outline=False):
        self.label_height = self.get_font_size() * 2
        self.setFixedHeight(self.label_height)
        border_style = "2px solid black" if outline else "none"
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.label_height // 2}px;"  # Adjust radius to maintain an oval shape
            f"  font-size: {self.get_font_size()}px;"
            f"  font-weight: bold;"
            f"  border: {border_style};"
            f"}}"
        )

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_label_style(outline=True)

    def leaveEvent(self, event: QEnterEvent) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_label_style()

    def resize_section_type_label(self) -> None:
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_height = self.get_font_size() * 2
        label_width = self.label_height * 5

        self.setFixedSize(label_width, self.label_height)
        self.set_label_style()
