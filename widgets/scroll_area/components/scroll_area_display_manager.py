import logging
from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Letters
from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)
from PyQt6.QtWidgets import QGridLayout

if TYPE_CHECKING:
    from ..scroll_area import CodexScrollArea
logging.basicConfig(level=logging.DEBUG)


class ScrollAreaDisplayManager:
    SPACING = 5
    COLUMN_COUNT = 8

    def __init__(self, scroll_area: "CodexScrollArea") -> None:
        self.scroll_area = scroll_area
        self.section_indices = {}  # Track indices for each section's grid layout

    def order_and_display_pictographs(self, letter_type: str) -> None:
        ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
        for key, pictograph in ordered_pictographs.items():
            self.add_pictograph_to_layout(pictograph)

    def add_pictograph_to_layout(self, pictograph: Pictograph) -> None:
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: SectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )

        if section:
            row_col = self.section_indices.get(letter_type, (0, 0))

            logging.debug(
                f"Before adding - {pictograph.letter}, {letter_type}: {row_col}"
            )

            section.pictograph_frame.layout.addWidget(
                pictograph.view, row_col[0], row_col[1]
            )

            col = row_col[1] + 1
            row = row_col[0] + (col // self.COLUMN_COUNT)
            col %= self.COLUMN_COUNT

            self.section_indices[letter_type] = (row, col)

            logging.debug(
                f"After adding - {letter_type}: {self.section_indices[letter_type]}"
            )

            pictograph.view.resize_for_scroll_area()

        else:
            self.scroll_area.sections_manager.create_section_if_needed(letter_type)

    def remove_pictograph(self, pictograph_key: str) -> None:
        pictograph_to_remove: Pictograph = self.scroll_area.pictographs.pop(
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
            for key in self.scroll_area.pictographs
            if key.split("_")[0] not in selected_letters
        ]

    def get_ordered_pictographs_for_section(
        self, letter_type: str
    ) -> dict[Letters, Pictograph]:
        # Filter the pictographs for the current section based on the letter type.
        return {
            k: v
            for k, v in sorted(
                self.scroll_area.pictographs.items(),
                key=lambda item: (
                    all_letters.index(item[1].letter),
                    item[1].start_pos,
                ),
            )
            if self.scroll_area.sections_manager.get_pictograph_letter_type(k)
            == letter_type
        }
