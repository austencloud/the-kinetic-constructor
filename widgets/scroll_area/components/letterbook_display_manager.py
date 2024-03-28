import logging
from typing import TYPE_CHECKING
from Enums.Enums import Letter

from widgets.pictograph.pictograph import Pictograph


from widgets.scroll_area.components.section_manager.section_widget.letterbook_section_widget import (
    LetterBookSectionWidget,
)

if TYPE_CHECKING:

    from ...letterbook.letterbook_scroll_area import LetterBookScrollArea
logging.basicConfig(level=logging.DEBUG)


class LetterBookDisplayManager:
    SPACING = 5
    COLUMN_COUNT = 8

    def __init__(self, scroll_area: "LetterBookScrollArea") -> None:
        self.scroll_area = scroll_area
        self.section_indices = {}  # Track indices for each section's grid layout

    def order_and_display_pictographs(self, section: LetterBookSectionWidget) -> None:
        ordered_pictographs = self.get_ordered_pictographs_for_section(section)
        for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(pictograph, index)

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = pictograph.letter_type
        section: LetterBookSectionWidget = (
            self.scroll_area.sections_manager.get_section(letter_type)
        )

        if section:
            row, col = divmod(index, self.COLUMN_COUNT)
            section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
            next_index = index + 1
            self.section_indices[letter_type] = divmod(next_index, self.COLUMN_COUNT)
            pictograph.view.resize_pictograph_view()

    def get_ordered_pictographs_for_section(
        self, section: LetterBookSectionWidget
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
