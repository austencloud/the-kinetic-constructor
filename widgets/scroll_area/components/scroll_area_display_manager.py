import logging
from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import (
    EIGHT_VARIATIONS,
    FOUR_VARIATIONS,
    SIXTEEN_VARIATIONS,
    all_letters,
)
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
        # Calculate the indices for the current section based on the selected letters.
        self.calculate_section_indices(letter_type)
        
        # Get the ordered pictographs for the current section.
        ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
        
        # Add each pictograph to the layout.
        for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: SectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )

        if section:
            # Calculate the row and column based on the index.
            row, col = divmod(index, self.COLUMN_COUNT)

            logging.debug(f"Adding {pictograph.letter} at position: ({row}, {col})")

            # Add the pictograph to the layout at the calculated position.
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)

            # Update the next available index for this section.
            next_index = index + 1
            self.section_indices[letter_type] = divmod(next_index, self.COLUMN_COUNT)

            # Resize the pictograph view as necessary.
            pictograph.view.resize_for_scroll_area()


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
                if letter in EIGHT_VARIATIONS
                else (
                    16
                    if letter in SIXTEEN_VARIATIONS
                    else 4 if letter in FOUR_VARIATIONS else 0
                )
            )
            for letter in selected_letters
        )

        # Reset the row and column indices for the section
        self.section_indices[letter_type] = (0, 0)

        # Calculate row and column for each pictograph
        for i in range(total_variations):
            row, col = divmod(i, self.COLUMN_COUNT)
            self.section_indices[letter_type] = (row, col)

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
