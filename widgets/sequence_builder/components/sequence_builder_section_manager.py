from typing import TYPE_CHECKING
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import Letters
from ...scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)
from ...scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder
    from widgets.sequence_builder.components.sequence_builder_scroll_area import (
        SequenceBuilderScrollArea,
    )


class SequenceBuilderSectionsManager:
    """Manages all of the sections in the scroll area. Individual sections are managed by the SectionWidget class."""

    SECTION_ORDER = [
        LetterType.Type1,
        LetterType.Type2,
        LetterType.Type3,
        LetterType.Type4,
        LetterType.Type5,
        LetterType.Type6,
    ]

    def __init__(self, scroll_area: "SequenceBuilderScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sequence_builder: "SequenceBuilder" = scroll_area.sequence_builder
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
        for letter_type in LetterType:
            self.create_section(letter_type)

    def create_section(self, letter_type: LetterType) -> SectionWidget:
        if letter_type not in self.sections:
            correct_index = self.get_correct_index_for_section(letter_type)
            section = SectionWidget(letter_type, self.scroll_area)
            self.scroll_area.add_widget_to_layout(section, correct_index)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            self.sections[letter_type] = section
            section.setup_components()

        return self.sections[letter_type]

    def get_correct_index_for_section(self, letter_type: LetterType) -> int:
        desired_position = self.SECTION_ORDER.index(letter_type)
        current_positions = [
            self.SECTION_ORDER.index(typ) for typ in self.ordered_section_types
        ]
        current_positions.sort()
        for i, pos in enumerate(current_positions):
            if pos >= desired_position:
                return i
        return len(self.ordered_section_types)

    def get_section(self, letter_type: LetterType) -> SectionWidget:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        if not section.filter_tab:
            if letter_type not in self.filter_tabs_cache:
                filter_tab = self.create_or_get_filter_tab(section)
                self.filter_tabs_cache[letter_type] = filter_tab
            section.filter_tab = self.filter_tabs_cache[letter_type]
        section.show()
        return section

    def get_pictograph_letter_type(self, pictograph_key: str) -> str:
        letter = pictograph_key.split("_")[0]
        for letter_type, letters in self.letters_by_type.items():
            if letter in letters:
                return letter_type
        return "Unknown"

    def clear_sections(self) -> None:
        """Clears all sections from the layout."""
        while self.scroll_area.container_layout.count():
            layout_item = self.scroll_area.container_layout.takeAt(0)
            if layout_item.widget():
                layout_item.widget().hide()
        self.sections.clear()

    def create_or_get_filter_tab(self, section: SectionWidget) -> FilterTab:
        if not section.filter_tab:
            section.filter_tab = FilterTab(section)
            section.layout.insertWidget(1, section.filter_tab)
        return section.filter_tab

    def show_all_sections(self) -> None:
        for section in self.sections.values():
            self.sequence_builder.scroll_area.container_layout.addWidget(section)
            section.show()
            section.resize_section()
