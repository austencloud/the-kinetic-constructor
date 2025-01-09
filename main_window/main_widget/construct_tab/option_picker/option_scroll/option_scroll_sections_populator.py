from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout


from Enums.Enums import LetterType
from .section_widget.option_picker_section_group_widget import OptionPickerSectionGroupWidget
from .section_widget.option_picker_section_widget import OptionPickerSectionWidget

if TYPE_CHECKING:
    from .option_scroll import OptionScroll


class OptionScrollSectionsPopulator:
    def __init__(self, option_scroll: "OptionScroll") -> None:
        self.option_scroll = option_scroll
        self.ordered_section_types: list[LetterType] = []
        self.initialize_sections()

    def initialize_sections(self) -> None:
        self._create_sections()
        self.add_sections_to_layout()

    def _create_sections(self):
        for letter_type in LetterType:
            section = OptionPickerSectionWidget(letter_type, self.option_scroll)
            self.option_scroll.sections[letter_type] = section
            self.ordered_section_types.append(letter_type)
            section.setup_components()

    def add_sections_to_layout(self) -> None:
        grouped_sections = [LetterType.Type4, LetterType.Type5, LetterType.Type6]
        group_widget = None

        for letter_type in list(LetterType):
            section = self.option_scroll.sections.get(letter_type)
            if section:
                if letter_type in grouped_sections:
                    if group_widget is None:
                        group_widget = OptionPickerSectionGroupWidget(
                            self.option_scroll
                        )
                        group_layout = QHBoxLayout()
                        group_layout.addStretch()
                        group_layout.addWidget(group_widget)
                        group_layout.addStretch()
                        self.option_scroll.layout.addLayout(group_layout, 3)
                    group_widget.add_section_widget(section)
                else:
                    self.option_scroll.layout.addWidget(section, 3)
