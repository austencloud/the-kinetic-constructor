from typing import TYPE_CHECKING, Dict, List
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import LetterTypes, Letters
from widgets.scroll_area.components.section_manager.section_widget.components.filter_tab import FilterTab
from .pictograph_organizer import PictographOrganizer
from .section_widget.section_widget import SectionWidget
from .section_organizer import SectionOrganizer

if TYPE_CHECKING:
    from ...scroll_area import ScrollArea


class ScrollAreaSectionManager:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area
        self.section_organizer = SectionOrganizer()
        self.pictograph_organizer = PictographOrganizer()
        self.sections: Dict[LetterTypes, SectionWidget] = {}
        self.filter_tab_cache: Dict[LetterTypes, SectionWidget] = {}
        self.ordered_section_types: List[LetterTypes] = []
        self.stretch_index = -1
        self.init_stretch()

    def init_stretch(self) -> None:
        if self.stretch_index != -1:
            self.scroll_area.layout.takeAt(self.stretch_index)
        self.scroll_area.layout.addStretch(1)
        self.stretch_index = self.scroll_area.layout.count() - 1

    def create_section_if_needed(self, letter_type: LetterTypes) -> None:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        if letter_type not in self.filter_tab_cache:
            filter_tab = self.create_or_get_filter_tab(section)
            self.filter_tab_cache[letter_type] = filter_tab
        else:
            filter_tab = self.filter_tab_cache[letter_type]
        self.update_sections_with_stretch()

    def create_or_get_filter_tab(self, section: SectionWidget) -> FilterTab:
        if not section.filter_tab:
            section.filter_tab = FilterTab(section)
            section.layout.insertWidget(1, section.filter_tab)
        return section.filter_tab

    def get_section(self, letter_type: LetterTypes) -> SectionWidget:
        return self.sections[letter_type]

    def create_section(self, letter_type: LetterTypes) -> None:
        if letter_type not in self.sections:
            section = SectionWidget(letter_type, self.scroll_area)
            correct_index = self.section_organizer.get_correct_index_for_section(
                letter_type, self.ordered_section_types
            )
            self.scroll_area.layout.addWidget(section)
            self.sections[letter_type] = section
            self.ordered_section_types.insert(correct_index, letter_type)
            self.update_sections_with_stretch()

    def update_sections_with_stretch(self):
        if self.stretch_index != -1:
            self.scroll_area.layout.takeAt(self.stretch_index)
        self.scroll_area.layout.addStretch(1)
        self.stretch_index = self.scroll_area.layout.count() - 1

    def update_sections_based_on_letters(self, selected_letters: List[Letters]) -> None:
        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            section = self.sections[letter_type]
            if letter_type not in self.sections:
                self.create_section(letter_type)
            section.show()
        for section in self.sections.values():
            for letter in selected_letters:
                letter_type = LetterType.get_letter_type(letter)
                if letter_type == section.letter_type:
                    break
            else:
                section.hide()
