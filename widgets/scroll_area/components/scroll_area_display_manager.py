from typing import TYPE_CHECKING, Dict, List
from widgets.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Letters
from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)

if TYPE_CHECKING:
    from ..scroll_area import ScrollArea


class ScrollAreaDisplayManager:
    COLUMN_COUNT = 8
    SPACING = 5

    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area

    def order_and_display_pictographs(self) -> None:
        ordered_pictographs = self.get_ordered_pictographs()
        for index, (key, codex_pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(codex_pictograph, index)

    def get_ordered_pictographs(self) -> Dict[Letters, Pictograph]:
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

    def add_pictograph_to_layout(
        self, codex_pictograph: Pictograph, index: int
    ) -> None:
        letter_type = self.scroll_area.section_manager.get_pictograph_letter_type(
            codex_pictograph.letter
        )
        section: SectionWidget = self.scroll_area.section_manager.sections.get(
            letter_type
        )
        if section:
            row = index // self.COLUMN_COUNT + 1
            col = index % self.COLUMN_COUNT
            section.pictograph_frame.layout.addWidget(codex_pictograph.view, row, col)
            codex_pictograph.view.resize_for_scroll_area()
        else:
            self.scroll_area.section_manager.create_section_if_needed(letter_type)

    def remove_pictograph(self, pictograph_key: str) -> None:
        codex_pictograph: Pictograph = self.scroll_area.pictographs.pop(
            pictograph_key, None
        )
        if codex_pictograph:
            self.scroll_area.layout.removeWidget(codex_pictograph.view)

    def clear_layout(self) -> None:
        while self.scroll_area.layout.count():
            widget = self.scroll_area.layout.takeAt(0).widget()
            if widget is not None:
                widget.setParent(None)

    def cleanup_unused_pictographs(self) -> None:
        keys_to_remove = self.get_keys_to_remove()
        for key in keys_to_remove:
            self.remove_pictograph(key)

    def get_keys_to_remove(self) -> List[str]:
        selected_letters = {
            letter.split("_")[0] for letter in self.scroll_area.codex.selected_letters
        }
        return [
            key
            for key in self.scroll_area.pictographs
            if key.split("_")[0] not in selected_letters
        ]

    def get_ordered_pictographs(self) -> Dict[Letters, Pictograph]:
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
