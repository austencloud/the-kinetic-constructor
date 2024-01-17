from typing import TYPE_CHECKING, Dict, List
from Enums import LetterNumberType
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    Letters,
)
from widgets.filter_tab.Type1_filter_tab import BaseFilterTab
from widgets.pictograph_scroll_area.scroll_area_section import ScrollAreaSection
from constants import Type1, Type2, Type3, Type4, Type5, Type6
from utilities.TypeChecking.TypeChecking import LetterTypeNums, Letters
from ..filter_tab.Type1_filter_tab import Type1FilterTab
from ..filter_tab.Type2_filter_tab import Type2FilterTab
from ..filter_tab.Type3_filter_tab import Type3FilterTab
from ..filter_tab.Type4_filter_tab import Type4FilterTab
from ..filter_tab.Type5_filter_tab import Type5FilterTab
from ..filter_tab.Type6_filter_tab import Type6FilterTab
from ..filter_tab.base_filter_tab import BaseFilterTab

if TYPE_CHECKING:
    from .scroll_area import ScrollArea

from PyQt6.QtWidgets import QLabel, QGridLayout, QSizePolicy


class ScrollAreaSectionManager:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area
        self.sections: Dict[LetterTypeNums, ScrollAreaSection] = {}
        self.letters_by_type = self.setup_letters_by_type()

        self.letters_by_type: Dict[
            LetterTypeNums, List[Letters]
        ] = self.setup_letters_by_type()
        self.pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        filter_tab_map = self.get_filter_tab_map()
        for letter_type, pictographs in self.pictographs_by_type.items():
            filter_tab = filter_tab_map.get(letter_type, BaseFilterTab)(
                self.scroll_area, letter_type
            )
            self.create_section(letter_type, filter_tab)

    def get_filter_tab_map(self) -> Dict[LetterTypeNums, BaseFilterTab]:
        filter_tab_map = {
            Type1: Type1FilterTab,
            Type2: Type2FilterTab,
            Type3: Type3FilterTab,
            Type4: Type4FilterTab,
            Type5: Type5FilterTab,
            Type6: Type6FilterTab,
        }

        return filter_tab_map

    def setup_letters_by_type(self) -> Dict[LetterTypeNums, List[Letters]]:
        letters_by_type = {}
        for letter_type in LetterNumberType:
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

    def create_section(
        self, letter_type: LetterTypeNums, filter_tab: BaseFilterTab
    ) -> None:
        # Instead of creating a QWidget, you will create an instance of the Section class
        section = ScrollAreaSection(letter_type, filter_tab, self.scroll_area)
        self.scroll_area.layout.addWidget(section)
        self.sections[letter_type] = section

    def create_section_label(self, styled_text: str) -> QLabel:
        """Creates a QLabel for the section label with the given styled text."""
        section_label = QLabel()
        section_label.setText(styled_text)  # Set the HTML styled text
        font_size = self.sections[0].calculate_font_size()
        section_label.setStyleSheet(f"font-size: {font_size}px; font-weight: bold;")
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        section_label.setSizePolicy(size_policy)
        section_label.setMinimumSize(section_label.sizeHint())
        return section_label

    def add_section_label_to_layout(
        self, section_label: QLabel, section_layout: QGridLayout
    ) -> None:
        """Adds the section label to the section layout."""
        section_layout.addWidget(
            section_label, 0, 0, 1, self.scroll_area.display_manager.COLUMN_COUNT
        )

    def get_section(self, letter_type: LetterTypeNums) -> ScrollAreaSection:
        return self.sections.get(letter_type)

    def organize_pictographs_by_type(self) -> None:
        for key, pictograph in self.scroll_area.pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            self.pictographs_by_type[letter_type].append(pictograph)

        for letter_type, pictographs in self.pictographs_by_type.items():
            for index, pictograph in enumerate(pictographs):
                self.scroll_area.display_manager.add_pictograph_to_layout(pictograph, index)