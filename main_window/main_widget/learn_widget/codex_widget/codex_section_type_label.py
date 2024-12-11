# section_type_label.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from Enums.letters import LetterType
from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.letter_type_text_painter import (
    LetterTypeTextPainter,
)

if TYPE_CHECKING:
    from main_window.main_widget.learn_widget.codex_widget.codex import Codex


class CodexSectionTypeLabel(QLabel):
    def __init__(self, codex: "Codex", letter_type: LetterType) -> None:
        super().__init__()
        self.codex = codex
        self.letter_type = letter_type
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.set_styled_text(letter_type)
        # self.set_label_style()

    def set_styled_text(self, letter_type: LetterType) -> None:
        # Use LetterTypeTextPainter to style the letter_type description
        styled_description = LetterTypeTextPainter.get_colored_text(
            letter_type.description
        )
        self.setText(f"{letter_type.name}: {styled_description}")

    def get_font_size(self):
        # Adjust font size based on codex height
        # This is arbitrary; you may adjust as per your layout
        return max(12, self.codex.height() // 45)

    def resizeEvent(self, event):
        # Setting a decent height and style for the label
        self.label_height = self.get_font_size() * 2
        self.setFixedHeight(self.label_height)
        border_style = "2px solid black"
        self.setStyleSheet(
            f"QLabel {{"
            f"  background-color: rgba(255, 255, 255, 200);"
            f"  border-radius: {self.label_height // 2}px;"
            f"  font-size: {self.get_font_size()}px;"
            f"  font-weight: bold;"
            f"  border: {border_style};"
            f"  padding: 0 10px;"
            f"}}"
        )

    # def enterEvent(self, event):
    #     self.setCursor(Qt.CursorShape.PointingHandCursor)
    #     self.set_label_style(outline=True)

    # def leaveEvent(self, event):
    #     self.setCursor(Qt.CursorShape.ArrowCursor)
    #     self.set_label_style()
