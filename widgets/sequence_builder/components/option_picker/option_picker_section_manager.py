from typing import TYPE_CHECKING
from Enums import LetterType
from utilities.TypeChecking.TypeChecking import Letters
from widgets.scroll_area.components.section_manager.section_widget.section_group_widget import (
    SectionGroupWidget,
)
from widgets.sequence_builder.components.option_picker.option_picker_section_widget import OptionPickerSectionWidget
from ....scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)


if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class OptionPickerSectionsManager:
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
        self.sequence_builder: "SequenceBuilder" = scroll_area.sequence_builder
        self.sections: dict[LetterType, OptionPickerSectionWidget] = {}
        self.filter_tabs_cache: dict[LetterType, FilterTab] = {}
        self.pictograph_cache: dict[Letters, list[LetterType]] = {}
        self.ordered_section_types: list[LetterType] = []

    def initialize_sections(self) -> None:
        for letter_type in LetterType:
            self.get_section(letter_type)

    def create_section(self, letter_type: LetterType) -> OptionPickerSectionWidget:
        if letter_type not in self.sections:
            section = OptionPickerSectionWidget(letter_type, self.scroll_area)
            self.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()
            # section.hide()
        return self.sections[letter_type]

    def add_sections_to_layout(self) -> None:
        grouped_sections = [LetterType.Type4, LetterType.Type5, LetterType.Type6]
        group_widget = None

        for section_type in self.SECTION_ORDER:
            section = self.sections.get(section_type)
            if section:
                # Group specified sections together
                if section_type in grouped_sections:
                    if group_widget is None:
                        group_widget = SectionGroupWidget()
                        correct_index = self.get_correct_index_for_section(
                            grouped_sections[0]
                        )
                        self.scroll_area.add_widget_to_layout(
                            group_widget, correct_index
                        )
                    group_widget.add_section_widget(section)
                else:
                    correct_index = self.get_correct_index_for_section(section_type)
                    self.scroll_area.add_widget_to_layout(section, correct_index)

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
        if not section.filter_tab:
            if letter_type not in self.filter_tabs_cache:
                filter_tab = self.create_or_get_filter_tab(section)
                self.filter_tabs_cache[letter_type] = filter_tab
            section.filter_tab = self.filter_tabs_cache[letter_type]
        return section

    def get_pictograph_letter_type(self, pictograph_key: str) -> str:
        letter = pictograph_key.split("_")[0]
        for letter_type in LetterType:
            if letter in letter_type.value[0]:
                return letter_type
        return "Unknown"

    def create_or_get_filter_tab(self, section: OptionPickerSectionWidget) -> FilterTab:
        if not section.filter_tab:
            section.filter_tab = FilterTab(section)
            section.layout.insertWidget(1, section.filter_tab)
        return section.filter_tab

    def show_all_sections(self) -> None:
        self.initialize_sections()
        self.add_sections_to_layout()
        for section in self.sections.values():
            section.show()
            section.resize_section()
            self.scroll_area.adjust_sections_size()
        self.scroll_area.fix_stretch()
