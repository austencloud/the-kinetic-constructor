import logging
from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letters

from widgets.pictograph.pictograph import Pictograph

from Enums.Enums import LetterType


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

    def order_and_display_pictographs(self, letter_type: LetterType) -> None:
        self.calculate_section_indices(letter_type)
        ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
        for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: CodexSectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )

        if section:
            row, col = divmod(index, self.COLUMN_COUNT)
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            next_index = index + 1
            self.section_indices[letter_type] = divmod(next_index, self.COLUMN_COUNT)
            pictograph.view.resize_pictograph_view()

    def calculate_section_indices(self, letter_type: str) -> None:
        selected_letters = [
            letter
            for letter in self.scroll_area.codex.selected_letters
            if self.scroll_area.sections_manager.get_pictograph_letter_type(letter)
            == letter_type
        ]

        total_variations = sum(
            (
                8
                if letter in Letters.get_letters_by_condition("eight_variations")
                else (
                    16
                    if letter in Letters.get_letters_by_condition("sixteen_variations")
                    else (
                        4
                        if letter in Letters.get_letters_by_condition("four_variations")
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

    def remove_pictograph(self, pictograph_key: str) -> None:
        pictograph_to_remove: Pictograph = self.scroll_area.pictograph_cache.pop(
            pictograph_key, None
        )
        if pictograph_to_remove:
            self.scroll_area.layout.removeWidget(pictograph_to_remove.view)

    def clear_layout(self) -> None:
        while self.scroll_area.layout.count():
            widget = self.scroll_area.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)

    def cleanup_unused_pictographs(self) -> None:
        keys_to_remove = self.get_keys_to_remove()
        for key in keys_to_remove:
            self.remove_pictograph(key)

    def get_keys_to_remove(self) -> list[str]:
        selected_letters = {
            letter.split("_")[0] for letter in self.scroll_area.codex.selected_letters
        }
        return [
            key
            for key in self.scroll_area.pictograph_cache
            if key.split("_")[0] not in selected_letters
        ]

    def get_ordered_pictographs_for_section(
        self, letter_type: LetterType
    ) -> dict[str, Pictograph]:
        ordered_pictographs = {
            k: v
            for k, v in sorted(
                self.scroll_area.pictograph_cache.items(),
                key=lambda item: (
                    list(Letters).index(Letters[item[1].letter]),
                    item[1].start_pos,
                ),
            )
            if self.scroll_area.sections_manager.get_pictograph_letter_type(k)
            == letter_type
        }
        return ordered_pictographs
