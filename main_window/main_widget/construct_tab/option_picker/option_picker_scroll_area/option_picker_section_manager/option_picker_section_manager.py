from typing import TYPE_CHECKING
from Enums.Enums import LetterType
from Enums.letters import Letter
from .option_picker_section_widget.option_picker_section_widget import (
    OptionPickerSectionWidget,
)
from ..option_picker_section_group_widget import OptionPickerSectionGroupWidget

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab import construct_tab

    from ..option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerSectionManager:
    """Manages all of the sections in the scroll area. Individual sections are managed by the OptionPickerSectionWidget class."""

    SECTION_ORDER = [
        LetterType.Type1,
        LetterType.Type2,
        LetterType.Type3,
        LetterType.Type4,
        LetterType.Type5,
        LetterType.Type6,
    ]

    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        self.scroll_area = scroll_area
        self.construct_tab: "construct_tab" = scroll_area.construct_tab
        self.sections: dict[LetterType, OptionPickerSectionWidget] = {}
        self.pictograph_cache: dict[Letter, list[LetterType]] = {}
        self.ordered_section_types: list[LetterType] = []
        self.initialized = False

    def initialize_sections(self) -> None:
        for letter_type in LetterType:
            self.get_section(letter_type)

    def create_section(self, letter_type: LetterType) -> OptionPickerSectionWidget:
        if letter_type not in self.sections:
            section = OptionPickerSectionWidget(letter_type, self.scroll_area)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()
        return self.sections[letter_type]

    def add_sections_to_layout(self) -> None:
        grouped_sections = [LetterType.Type4, LetterType.Type5, LetterType.Type6]
        group_widget = None

        for section_type in self.SECTION_ORDER:
            section = self.sections.get(section_type)
            if section:
                if section_type in grouped_sections:
                    if group_widget is None:
                        group_widget = OptionPickerSectionGroupWidget(self.scroll_area)
                        correct_index = self.get_correct_index_for_section(
                            grouped_sections[0]
                        )
                        self.scroll_area.add_section_to_layout(
                            group_widget, correct_index
                        )
                    group_widget.add_section_widget(section)
                else:
                    correct_index = self.get_correct_index_for_section(section_type)
                    self.scroll_area.add_section_to_layout(section, correct_index)

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

    def get_section(self, letter_type: LetterType) -> OptionPickerSectionWidget:
        if letter_type not in self.sections:
            self.create_section(letter_type)
        section = self.sections[letter_type]
        return section

    def get_pictograph_letter_type(self, letter: Letter) -> str:
        letter_str = letter.value
        for letter_type in LetterType:
            if letter_str in letter_type.value[0]:
                return letter_type
        return "Unknown"

    def show_all_sections(self) -> None:
        if not self.initialized:
            self.initialize_sections()
            self.add_sections_to_layout()
            self.initialized = True
        for section in self.sections.values():
            section.show()
            section.resize_option_picker_section_widget()
