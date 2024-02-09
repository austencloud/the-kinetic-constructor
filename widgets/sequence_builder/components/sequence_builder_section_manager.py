from typing import TYPE_CHECKING
from Enums import LetterType
from constants import BLUE_TURNS, RED_TURNS
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph.pictograph import Pictograph
from ...scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)
from ...scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)
from PyQt6.QtWidgets import QGridLayout, QLabel

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder
    from widgets.sequence_builder.components.sequence_builder_scroll_area import (
        SequenceBuilderScrollArea,
    )


class SequenceBuilderScrollAreaSectionsManager:
    """Manages all of the sections in the scroll area. Individual sections are managed by the SectionWidget class."""

    SECTION_ORDER = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"]

    def __init__(self, scroll_area: "SequenceBuilderScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: dict[LetterType, SectionWidget] = {}
        self.filter_tabs_cache: dict[LetterType, FilterTab] = {}
        self.pictograph_cache: dict[Letters, list[LetterType]] = {}
        self.letters_by_type: dict[LetterType, list[Letters]] = (
            self.setup_letters_by_type()
        )
        self.pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        self.ordered_section_types: list[LetterType] = []
        self.initialize_sections()

    def setup_letters_by_type(self) -> dict[LetterType, list[Letters]]:
        letters_by_type = {}
        for letter_type in LetterType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

    def initialize_sections(self) -> None:
        # Create a section for each letter type upfront
        for letter_type in LetterType:
            self.create_section(letter_type)

    def create_section(self, letter_type: LetterType) -> SectionWidget:
        if letter_type not in self.sections:
            correct_index = self.get_correct_index_for_section(letter_type)
            section = SectionWidget(letter_type, self.scroll_area)
            self.scroll_area.insert_widget_at_index(section, correct_index)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()
            self.sections[letter_type] = section

        return self.sections[letter_type]

    def get_correct_index_for_section(self, letter_type: LetterType) -> int:
        desired_position = self.SECTION_ORDER.index(letter_type.name)
        current_positions = [
            self.SECTION_ORDER.index(typ.name) for typ in self.ordered_section_types
        ]
        current_positions.sort()
        for i, pos in enumerate(current_positions):
            if pos >= desired_position:
                return i
        return len(self.ordered_section_types)

    def get_section(self, letter_type: LetterType) -> SectionWidget:
        return self.create_section_if_needed(letter_type)

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

    def create_section_if_needed(self, letter_type: LetterType) -> None:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        if not section.filter_tab:
            if letter_type not in self.filter_tabs_cache:
                filter_tab = self.create_or_get_filter_tab(section)
                self.filter_tabs_cache[letter_type] = filter_tab
            section.filter_tab = self.filter_tabs_cache[letter_type]

    def update_sections_based_on_letters(self, selected_letters: list[Letters]) -> None:
        sections_to_show = self.get_sections_to_show_from_selected_letters(
            selected_letters
        )

        for section in self.sections.values():
            if section.letter_type in sections_to_show:
                if section.isHidden():
                    section.show()
            else:
                section.hide()
                for pictograph in section.pictographs.values():
                    pictograph.updater.update_pictograph({RED_TURNS: 0, BLUE_TURNS: 0})

        self.scroll_area.fix_stretch()

    def get_sections_to_show_from_selected_letters(
        self, selected_letters: list[Letters]
    ) -> list[LetterType]:
        sections_to_show = []
        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            if letter_type not in sections_to_show:
                sections_to_show.append(letter_type)
        return sections_to_show

    def create_or_get_filter_tab(self, section: SectionWidget) -> FilterTab:
        if not section.filter_tab:
            section.filter_tab = FilterTab(section)
            section.layout.insertWidget(1, section.filter_tab)
        return section.filter_tab

    def update_sections_for_sequence_context(self, end_pos: str):
        # Filter pictographs for each section based on `end_pos`
        for letter_type, section in self.sections.items():
            valid_pictographs = self._filter_pictographs_for_next_step(
                end_pos, letter_type
            )
            section.update_with_pictographs(valid_pictographs)

    def _filter_pictographs_for_next_step(self, end_pos: str, letter_type: str):
        valid_pictographs = []
        # Example logic to select pictographs based on end_pos and specific rules
        for pictograph in self.available_pictographs[letter_type]:
            if pictograph.start_pos == end_pos:  # Simplified check
                valid_pictographs.append(pictograph)
        return valid_pictographs
