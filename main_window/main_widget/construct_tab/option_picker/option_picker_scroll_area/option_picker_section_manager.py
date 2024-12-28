from typing import TYPE_CHECKING
from Enums.Enums import LetterType
from Enums.letters import Letter
from .option_picker_section_group_widget import OptionPickerSectionGroupWidget
from .option_picker_section_widget import OptionPickerSectionWidget
from PyQt6.QtWidgets import QHBoxLayout

if TYPE_CHECKING:

    from .option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerSectionManager:
    """Manages all of the sections in the scroll area. Individual sections are managed by the OptionPickerSectionWidget class."""

    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        self.scroll_area = scroll_area
        self.manual_builder = scroll_area.manual_builder
        self.sections: dict[LetterType, OptionPickerSectionWidget] = {}
        self.pictograph_cache: dict[Letter, list[LetterType]] = {}
        self.ordered_section_types: list[LetterType] = []
        self.initialized = False
        self.initialize_sections()

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

        for letter_type in list(LetterType):
            section = self.sections.get(letter_type)
            if section:
                if letter_type in grouped_sections:
                    if group_widget is None:
                        group_widget = OptionPickerSectionGroupWidget(self.scroll_area)
                        group_layout = QHBoxLayout()
                        group_layout.addStretch()
                        group_layout.addWidget(group_widget)
                        group_layout.addStretch()
                        self.scroll_area.layout.addLayout(group_layout)
                    group_widget.add_section_widget(section)
                else:
                    self.scroll_area.layout.addWidget(section)

    def get_correct_index_for_section(self, letter_type: LetterType) -> int:
        desired_position = list(LetterType).index(letter_type)
        current_positions = [
            list(LetterType).index(typ) for typ in self.ordered_section_types
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

    def display_sections(self) -> None:
        if not self.initialized:
            self.add_sections_to_layout()
            self.initialized = True
        for section in self.sections.values():
            section.show()
