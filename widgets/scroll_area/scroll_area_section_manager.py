from typing import TYPE_CHECKING, Dict, List
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import LetterTypes, Letters
from widgets.scroll_area.scroll_area_section import ScrollAreaSection
from ..filter_tab import FilterTab

if TYPE_CHECKING:
    from .scroll_area import ScrollArea

from PyQt6.QtWidgets import QLabel, QGridLayout


class ScrollAreaSectionManager:
    
    SECTION_ORDER = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]

    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: Dict[LetterTypes, ScrollAreaSection] = {}
        self.filter_tabs_cache: Dict[LetterTypes, FilterTab] = {}
        self.letters_by_type: Dict[
            LetterTypes, List[Letters]
        ] = self.setup_letters_by_type()
        self.pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        self.ordered_section_types = []  # Keep track of the order of added sections

    def setup_letters_by_type(self) -> Dict[LetterTypes, List[Letters]]:
        letters_by_type = {}
        for letter_type in LetterType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

    def initialize_sections(self) -> None:
        for letter_type in self.letters_by_type:
            self.create_section(letter_type)


    def create_section(self, letter_type: LetterTypes) -> ScrollAreaSection:
        if letter_type not in self.sections:
            # Determine the correct index for the new section
            correct_index = self.get_correct_index_for_section(letter_type)
            section = ScrollAreaSection(letter_type, self.scroll_area)
            self.scroll_area.insert_widget_at_index(section, correct_index)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)

            # Ensure the stretch is still at the end
            self.scroll_area.update_sections()

        return self.sections[letter_type]
    
    
    def get_correct_index_for_section(self, letter_type: LetterTypes) -> int:
        try:
            # Find the index where this section should be inserted
            desired_position = self.SECTION_ORDER.index(letter_type)
            current_positions = [self.SECTION_ORDER.index(typ) for typ in self.ordered_section_types]
            insert_before = next((i for i, pos in enumerate(current_positions) if pos > desired_position), len(self.ordered_section_types))
            return insert_before
        except ValueError:
            # If the letter_type is not in SECTION_ORDER, append at the end
            return len(self.ordered_section_types)
    def get_section(self, letter_type: LetterTypes) -> ScrollAreaSection:
        return self.create_section(letter_type)

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

    def create_section_if_needed(self, letter_type: LetterTypes) -> None:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        if not section.filter_tab:
            section.create_or_get_filter_tab()

    def update_sections_based_on_letters(self, selected_letters: List[Letters]) -> None:
        # First, hide all sections and filter tabs
        for section in self.sections.values():
            section.hide()
            section.hide_filter_tab()

        # Now, show only the sections and filter tabs needed based on selected letters
        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            if letter_type in self.sections:
                self.sections[letter_type].show()
                self.sections[letter_type].show_filter_tab()
        self.scroll_area.update_sections()
