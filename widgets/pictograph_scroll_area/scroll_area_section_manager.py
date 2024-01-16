from typing import TYPE_CHECKING, Dict, List
from Enums import LetterNumberType
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    Letters,
)
from widgets.filter_frame.filter_tab.filter_tab import FilterTab
from widgets.pictograph_scroll_area.scroll_area_section import ScrollAreaSection

if TYPE_CHECKING:
    from .pictograph_scroll_area import PictographScrollArea

from PyQt6.QtWidgets import QLabel, QGridLayout, QSizePolicy


class ScrollAreaSectionManager:
    def __init__(self, scroll_area: "PictographScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: Dict[LetterTypeNums, ScrollAreaSection] = {}
        self.letters_by_type = self.setup_letters_by_type()

    def setup_letters_by_type(self) -> Dict[LetterTypeNums, List[Letters]]:
        letters_by_type = {}
        for letter_type in LetterNumberType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

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

    def create_section(
        self, letter_type: LetterTypeNums, filter_tab: FilterTab
    ) -> None:
        # Instead of creating a QWidget, you will create an instance of the Section class
        section = ScrollAreaSection(letter_type, filter_tab, self.scroll_area)
        self.scroll_area.layout.addWidget(section)
        self.sections[letter_type] = section

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

