import logging
from typing import TYPE_CHECKING
from Enums.Enums import Letter

from Enums.letters import LetterConditions
from widgets.pictograph.pictograph import Pictograph


from widgets.scroll_area.components.section_manager.section_widget.codex_section_widget import (
    CodexSectionWidget,
)

if TYPE_CHECKING:

    from ..codex_scroll_area import CodexScrollArea
logging.basicConfig(level=logging.DEBUG)


class CodexDisplayManager:
    SPACING = 5
    COLUMN_COUNT = 8

    def __init__(self, scroll_area: "CodexScrollArea") -> None:
        self.scroll_area = scroll_area
        self.section_indices = {}  # Track indices for each section's grid layout

    def order_and_display_pictographs(self, section: CodexSectionWidget) -> None:
        self.calculate_section_indices(section)
        ordered_pictographs = self.get_ordered_pictographs_for_section(section)
        for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = pictograph.letter_type
        section: CodexSectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )

        if section:
            row, col = divmod(index, self.COLUMN_COUNT)
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            next_index = index + 1
            self.section_indices[letter_type] = divmod(next_index, self.COLUMN_COUNT)
            pictograph.view.resize_pictograph_view()

    def calculate_section_indices(self, section: CodexSectionWidget) -> None:
        letter_type = section.letter_type
        selected_letters = [
            letter
            for letter in self.scroll_area.codex.selected_letters
            if self.scroll_area.sections_manager.get_pictograph_letter_type(letter)
            == letter_type
        ]

        total_variations = sum(
            (
                8
                if letter
                in Letter.get_letters_by_condition(LetterConditions.EIGHT_VARIATIONS)
                else (
                    16
                    if letter
                    in Letter.get_letters_by_condition(
                        LetterConditions.SIXTEEN_VARIATIONS
                    )
                    else (
                        4
                        if letter
                        in Letter.get_letters_by_condition(
                            LetterConditions.FOUR_VARIATIONS
                        )
                        else 0
                    )
                )
            )
            for letter in selected_letters
        )

        self.section_indices[letter_type] = (0, 0)
        for i in range(total_variations):
            row, col = divmod(i, self.COLUMN_COUNT)
            self.section_indices[letter_type] = (row, col)

    def get_ordered_pictographs_for_section(
        self, section: CodexSectionWidget
    ) -> dict[str, Pictograph]:
        ordered_pictographs = {
            k: v
            for k, v in sorted(
                self.scroll_area.pictograph_cache.items(),
                key=lambda item: (
                    list(Letter).index(item[1].letter),
                    item[1].start_pos,
                ),
            )
            if self.scroll_area.sections_manager.get_pictograph_letter_type(v.letter)
            == section.letter_type
        }
        return ordered_pictographs
