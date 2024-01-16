from typing import TYPE_CHECKING, Dict, List
from Enums import LetterNumberType
from utilities.TypeChecking.TypeChecking import (
    Letters,
)
from widgets.filter_frame.filter_tab.filter_tab import ScrollAreaFilterTab
from ..ig_tab.ig_scroll.ig_pictograph import IGPictograph

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area_display_manager import (
        ScrollAreaDisplayManager,
    )
    from .pictograph_scroll_area import PictographScrollArea

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout, QSizePolicy


class ScrollAreaSectionManager:
    def __init__(self, scroll_area: "PictographScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: Dict[str, QGridLayout] = {}
        self.letters_by_type: Dict[str, List[str]] = self.setup_letters_by_type()

    def setup_letters_by_type(self) -> Dict[str, List[str]]:
        letters_by_type = {}
        for letter_type in LetterNumberType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

    def organize_pictographs_by_type(
        self, pictographs: Dict[Letters, IGPictograph]
    ) -> None:
        self.clear_sections()
        pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        for key, pictograph in pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            pictographs_by_type[letter_type].append(pictograph)

        for letter_type, pictographs in pictographs_by_type.items():
            self.create_section(letter_type)
            for index, pictograph in enumerate(pictographs):
                self.scroll_area.display_manager.add_pictograph_to_layout(
                    pictograph, index
                )

    def get_pictograph_letter_type(self, pictograph_key: str) -> str:
        letter = pictograph_key.split("_")[0]
        for letter_type, letters in self.letters_by_type.items():
            if letter in letters:
                return letter_type
        return "Unknown"

    def clear_sections(self) -> None:
        """Clears all sections from the layout."""
        while self.scroll_area.layout.count():
            layout_item = self.scroll_area.layout.takeAt(0)
            if layout_item.widget():
                layout_item.widget().hide()
        self.sections.clear()

    def create_section(self, letter_type: str, filter_tab: ScrollAreaFilterTab) -> None:
        """Creates a new section for a given letter type."""
        section_frame = QWidget()
        section_layout = QGridLayout(section_frame)
        styled_text = self.get_styled_text(letter_type)
        section_label = self.create_section_label(styled_text)
        self.add_section_label_to_layout(section_label, section_layout)
        self.scroll_area.layout.addWidget(filter_tab)
        self.scroll_area.layout.addWidget(section_frame)
        self.scroll_area.sections[letter_type] = section_layout

    def get_styled_text(self, letter_type: str) -> str:
        """Returns the styled text for the section label."""
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
            "Static": "#ff4000",  # orange
            "-": "#000000",
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
        return styled_text

    def create_section_label(self, styled_text: str) -> QLabel:
        """Creates a QLabel for the section label with the given styled text."""
        section_label = QLabel()
        section_label.setText(styled_text)  # Set the HTML styled text
        font_size = self.calculate_font_size()
        section_label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        section_label.setSizePolicy(size_policy)
        section_label.setMinimumSize(section_label.sizeHint())
        return section_label

    def add_section_label_to_layout(
        self, section_label: QLabel, section_layout: QGridLayout
    ) -> None:
        """Adds the section label to the section layout."""
        section_layout.addWidget(
            section_label, 0, 0, 1, self.scroll_area.display_manager.COLUMN_COUNT
        )

    def calculate_font_size(self) -> int:
        window_width = self.scroll_area.width()
        font_size = window_width // 50
        return font_size
