from typing import TYPE_CHECKING, Dict, List
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import LetterTypes, Letters
from widgets.scroll_area.scroll_area_section import ScrollAreaSection
from ..filter_tab import FilterTab

if TYPE_CHECKING:
    from .scroll_area import ScrollArea

from PyQt6.QtWidgets import QLabel, QGridLayout


class ScrollAreaSectionManager:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: Dict[LetterTypes, ScrollAreaSection] = {}
        self.letters_by_type = self.setup_letters_by_type()

        self.letters_by_type: Dict[
            LetterTypes, List[Letters]
        ] = self.setup_letters_by_type()
        self.pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        for letter_type, _ in self.pictographs_by_type.items():
            self.create_section(letter_type)

    def setup_letters_by_type(self) -> Dict[LetterTypes, List[Letters]]:
        letters_by_type = {}
        for letter_type in LetterType:
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

    def create_section(self, letter_type: LetterTypes) -> ScrollAreaSection:
        section = ScrollAreaSection(letter_type, self.scroll_area)
        self.scroll_area.layout.addWidget(section)
        self.sections[letter_type] = section
        return section

    def add_section_label_to_layout(
        self, section_label: QLabel, section_layout: QGridLayout
    ) -> None:
        """Adds the section label to the section layout."""
        section_layout.addWidget(
            section_label, 0, 0, 1, self.scroll_area.display_manager.COLUMN_COUNT
        )

    def get_section(self, letter_type: LetterTypes) -> ScrollAreaSection:
        return self.sections.get(letter_type)

    def organize_pictographs_by_type(self) -> None:
        for key, pictograph in self.scroll_area.pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            self.pictographs_by_type[letter_type].append(pictograph)

        for letter_type, pictographs in self.pictographs_by_type.items():
            for index, pictograph in enumerate(pictographs):
                self.scroll_area.display_manager.add_pictograph_to_layout(
                    pictograph, index
                )
