import logging
from typing import TYPE_CHECKING
from Enums import LetterType
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

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )


class OptionPickerDisplayManager:
    SPACING = 5
    COLUMN_COUNT = 8

    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:

        self.scroll_area = scroll_area
        self.section_indices = {}  # Track indices for each section's grid layout

    def order_and_display_pictographs(self) -> None:
        for letter_type in LetterType:
            self.calculate_section_indices(letter_type)
            ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
            for index, (key, pictograph_tuple) in enumerate(ordered_pictographs.items()):
                self.add_pictograph_to_layout(pictograph_tuple[0], index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: SectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )

        if section:
            row, col = divmod(index, self.COLUMN_COUNT)
            logging.debug(f"Adding {pictograph.letter} at position: ({row}, {col})")
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            next_index = index + 1
            self.section_indices[letter_type] = divmod(next_index, self.COLUMN_COUNT)
            pictograph.view.resize_for_scroll_area()

    def calculate_section_indices(self, letter_type: str) -> None:

        total_variations = sum(
            (
                8
                if pictograph.letter in EIGHT_VARIATIONS
                else (
                    16
                    if pictograph.letter in SIXTEEN_VARIATIONS
                    else 4 if pictograph.letter in FOUR_VARIATIONS else 0
                )
            )
            for pictograph, _ in self.scroll_area.pictographs.values()
        )

        self.section_indices[letter_type] = (0, 0)
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

    def get_ordered_pictographs(self) -> dict[Letters, Pictograph]:
        return {
            k: v
            for k, v in sorted(
                self.scroll_area.pictographs.items(),
                key=lambda item: (
                    all_letters.index(item[1].letter),
                    item[1].start_pos,
                ),
            )
        }

    def get_ordered_pictographs_for_section(
        self, letter_type: LetterType
    ) -> dict[Letters, Pictograph]:
        return {
            k: v
            for k, v in sorted(
                self.scroll_area.pictographs.items(),
                key=lambda item: (
                    all_letters.index(item[1][0].letter),
                    item[1][0].start_pos,
                ),
            )
            if self.scroll_area.sections_manager.get_pictograph_letter_type(k)
            == letter_type
        }
