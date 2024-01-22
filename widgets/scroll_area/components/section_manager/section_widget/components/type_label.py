from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import SectionWidget


class ScrollAreaSectionTypeLabel(QLabel):
    TYPE_MAP = {
        "Type1": "Dual-Shift",
        "Type2": "Shift",
        "Type3": "Cross-Shift",
        "Type4": "Dash",
        "Type5": "Dual-Dash",
        "Type6": "Static",
    }

    COLORS = {
        "Shift": "#6F2DA8",  # purple
        "Dual": "#00b3ff",  # cyan
        "Dash": "#26e600",  # green
        "Cross": "#26e600",  # green
        "Static": "#eb7d00",  # orange
        "-": "#000000",  # black
    }

    def __init__(self, scroll_area_section: "SectionWidget") -> None:
        super().__init__()
        self.set_styled_text(scroll_area_section.letter_type)

    def set_styled_text(self, letter_type: str) -> None:
        type_words = self.TYPE_MAP.get(letter_type, "").split("-")

        styled_words = [
            f"<span style='color: {self.COLORS.get(word, 'black')};'>{word}</span>"
            for word in type_words
        ]

        styled_type_name = "-".join(styled_words) if "-" in self.TYPE_MAP.get(letter_type, "") else "".join(styled_words)

        styled_text = f"{letter_type[0:4]} {letter_type[4]}: {styled_type_name}"
        self.setText(styled_text)
        font_size = 30
        self.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed))
        self.setMinimumSize(self.sizeHint())
