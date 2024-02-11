from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

from Enums import LetterType


if TYPE_CHECKING:
    from ..codex_section_widget import CodexSectionWidget
from PyQt6.QtCore import pyqtSignal


class SectionTypeLabel(QLabel):
    clicked = pyqtSignal()

    TYPE_MAP = {
        LetterType.Type1: "Dual-Shift",
        LetterType.Type2: "Shift",
        LetterType.Type3: "Cross-Shift",
        LetterType.Type4: "Dash",
        LetterType.Type5: "Dual-Dash",
        LetterType.Type6: "Static",
    }

    COLORS = {
        "Shift": "#6F2DA8",  # purple
        "Dual": "#00b3ff",  # cyan
        "Dash": "#26e600",  # green
        "Cross": "#26e600",  # green
        "Static": "#eb7d00",  # orange
        "-": "#000000",  # black
    }

    def __init__(self, section_widget: "CodexSectionWidget") -> None:
        super().__init__()
        self.section = section_widget
        self.set_styled_text(section_widget.letter_type)

    def set_styled_text(self, letter_type: LetterType) -> None:
        type_words = self.TYPE_MAP.get(letter_type, "").split("-")
        letter_type_str = letter_type.name
        styled_words = [
            f"<span style='color: {self.COLORS.get(word, 'black')};'>{word}</span>"
            for word in type_words
        ]

        styled_type_name = (
            "-".join(styled_words)
            if "-" in self.TYPE_MAP.get(letter_type, "")
            else "".join(styled_words)
        )

        styled_text = f"{letter_type_str[0:4]} {letter_type_str[4]}: {styled_type_name}"
        self.setText(styled_text)
        self.resize_type_label()

    def resize_type_label(self) -> None:
        base_class_name = type(self.section.scroll_area).__name__
        if base_class_name == "CodexScrollArea":
            font_size = self.section.scroll_area.width() // 40
        elif base_class_name == "OptionPickerScrollArea":
            font_size = self.section.scroll_area.width() // 50
        else:
            font_size = 12

        self.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()
        super().mousePressEvent(event)
