from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

from constants import BLUE_TURNS, RED_TURNS
from Enums.Enums import LetterType


from .section_widget.components.turns_tab.turns_tab import TurnsTab
from .section_widget.codex_section_widget import CodexSectionWidget
from PyQt6.QtWidgets import QGridLayout, QLabel

if TYPE_CHECKING:
    from ...codex_scroll_area import CodexScrollArea


class CodexSectionManager:
    """Manages all of the sections in the scroll area. Individual sections are managed by the SectionWidget class."""

    SECTION_ORDER = [
        LetterType.Type1,
        LetterType.Type2,
        LetterType.Type3,
        LetterType.Type4,
        LetterType.Type5,
        LetterType.Type6,
    ]

    def __init__(self, scroll_area: "CodexScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: dict[LetterType, CodexSectionWidget] = {}
        self.filter_tabs_cache: dict[LetterType, TurnsTab] = {}
        self.pictograph_cache: dict[Letter, list[LetterType]] = {}

        self.pictographs_by_type = {type: [] for type in LetterType}
        self.ordered_section_types: list[LetterType] = []

    def create_section(self, letter_type: LetterType) -> CodexSectionWidget:
        if letter_type not in self.sections:
            correct_index = self.get_correct_index_for_section(letter_type)
            section = CodexSectionWidget(letter_type, self.scroll_area)
            self.scroll_area.insert_widget_at_index(section, correct_index)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()
            self.sections[letter_type] = section

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

    def get_pictograph_letter_type(self, letter: Letter) -> LetterType:
        letter_str = Letter.get_letter(letter)
        return LetterType.get_letter_type(letter_str)

    def add_section_label_to_layout(
        self, section_label: QLabel, section_layout: QGridLayout
    ) -> None:
        column_count = self.scroll_area.display_manager.COLUMN_COUNT
        section_layout.addWidget(section_label, 0, 0, 1, column_count)

    def get_section(self, letter_type: LetterType) -> CodexSectionWidget:
        return self.sections.get(letter_type)

    def create_section_if_needed(self, letter_type: LetterType) -> None:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        if not section.turns_tab:
            if letter_type not in self.filter_tabs_cache:
                turns_tab = self.create_or_get_turns_tab(section)
                self.filter_tabs_cache[letter_type] = turns_tab
            section.turns_tab = self.filter_tabs_cache[letter_type]

    def update_sections_based_on_letters(self, selected_letters: list[Letter]) -> None:
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
        self, selected_letters: list[Letter]
    ) -> list[LetterType]:
        sections_to_show = []
        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            if letter_type not in sections_to_show:
                sections_to_show.append(letter_type)
        return sections_to_show

    def create_or_get_turns_tab(self, section: CodexSectionWidget) -> TurnsTab:
        if not section.turns_tab:
            section.turns_tab = TurnsTab(section)
            section.layout.insertWidget(1, section.turns_tab)
        return section.turns_tab
