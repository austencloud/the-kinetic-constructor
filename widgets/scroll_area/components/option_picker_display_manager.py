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
from widgets.sequence_builder.components.option_picker.option_picker_section_widget import (
    OptionPickerSectionWidget,
)

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )


class OptionPickerDisplayManager:
    SPACING = 5
    COLUMN_COUNT = 8

    def __init__(self, scroll_area: "OptionPickerScrollArea"):
        self.scroll_area = scroll_area
        self.section_indices = {}
        self.pictograph_count = 0

    def order_and_display_pictographs(self):
        for letter_type in LetterType:
            self.calculate_section_indices(letter_type)
            ordered_pictographs = self.get_ordered_pictographs_for_section(letter_type)
            for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
                self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int):
        row, col = divmod(index, self.COLUMN_COUNT)
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: SectionWidget = self.scroll_area.sections_manager.get_section(
            letter_type
        )
        if section:
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            pictograph.view.resize_for_scroll_area()
            pictograph.view.show()

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
            for pictograph in self.scroll_area.pictograph_cache.values()
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

    def get_ordered_pictographs(self) -> dict[Letters, Pictograph]:
        return {
            k: v
            for k, v in sorted(
                self.scroll_area.pictograph_cache.items(),
                key=lambda item: (
                    all_letters.index(item[1].letter),
                    item[1].start_pos,
                ),
            )
        }

    def get_ordered_pictographs_for_section(
        self, letter_type: LetterType
    ) -> dict[str, Pictograph]:
        """Returns pictographs ordered by their letter and start position for a given section type,
        but only if they are relevant to the current_pictograph's end position."""
        current_pictograph = self.scroll_area.sequence_builder.current_pictograph
        relevant_pictographs = {}

        for key, pictograph in self.scroll_area.pictograph_cache.items():
            if self.is_pictograph_relevant(pictograph, current_pictograph):
                if (
                    self.scroll_area.sections_manager.get_pictograph_letter_type(key)
                    == letter_type
                ):
                    relevant_pictographs[key] = pictograph

        return {
            k: v
            for k, v in sorted(
                relevant_pictographs.items(),
                key=lambda item: (
                    all_letters.index(item[1].letter),
                    item[1].start_pos,
                ),
            )
        }

    def is_pictograph_relevant(
        self, pictograph: Pictograph, current_pictograph: Pictograph
    ) -> bool:
        """Check if a pictograph is a valid next option based on the current_pictograph."""

        if (
            current_pictograph.end_pos == pictograph.start_pos
            and current_pictograph.red_motion.end_ori == pictograph.red_motion.start_ori
            and current_pictograph.blue_motion.end_ori
            == pictograph.blue_motion.start_ori
        ):
            return True

    def clear_all_section_layouts(self):
        """Clears all widgets from all section layouts."""
        for section in self.scroll_area.sections_manager.sections.values():
            section.clear_pictographs()

    def add_pictograph_to_section_layout(self, pictograph: Pictograph):
        """Add a pictograph to its corresponding section layout."""
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: OptionPickerSectionWidget = (
            self.scroll_area.sections_manager.get_section(letter_type)
        )
        if section:
            section.add_pictograph(pictograph)
