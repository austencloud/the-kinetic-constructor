# Import necessary components
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QLabel,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import LetterTypes

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import SectionWidget


class ScrollAreaSectionTypeLabel(QLabel):
    def __init__(self, scroll_area_section: "SectionWidget"):
        super().__init__()
        self.setStyledText(scroll_area_section.letter_type)

    def setStyledText(self, letter_type: LetterTypes) -> None:
        type_map = {
            "Type1": "Dual-Shift",
            "Type2": "Shift",
            "Type3": "Cross-Shift",
            "Type4": "Dash",
            "Type5": "Dual-Dash",
            "Type6": "Static",
        }

        colors = {
            "Shift": "#6F2DA8",  # purple
            "Dual": "#00b3ff",  # cyan
            "Dash": "#26e600",  # green
            "Cross": "#26e600",  # green
            "Static": "#eb7d00",  # orange
            "-": "#000000",  # black
        }

        type_words = type_map[letter_type].split("-")

        styled_words = []
        for word in type_words:
            color = colors.get(word, "black")
            styled_words.append(f"<span style='color: {color};'>{word}</span>")

        styled_type_name = (
            "-".join(styled_words)
            if "-" in type_map[letter_type]
            else "".join(styled_words)
        )

        styled_text = f"{letter_type[0:4]} {letter_type[4]}: {styled_type_name}"
        self.setText(styled_text)
        font_size = 30
        self.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.setSizePolicy(size_policy)
        self.setMinimumSize(self.sizeHint())
