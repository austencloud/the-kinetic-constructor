from typing import TYPE_CHECKING
from widgets.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import all_letters
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

    def order_and_display_pictographs(self) -> None:
        ordered_pictographs = self.get_ordered_pictographs()
        for index, (key, pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(pictograph, index)

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

    def add_pictograph_to_layout(self, pictograph: Pictograph, index: int) -> None:
        letter_type = self.scroll_area.sections_manager.get_pictograph_letter_type(
            pictograph.letter
        )
        section: SectionWidget = self.scroll_area.sections_manager.sections.get(
            letter_type
        )
        row = index // self.COLUMN_COUNT + 1
        col = index % self.COLUMN_COUNT
        section.pictograph_frame.layout.addWidget(pictograph.view, row, col)
        pictograph.view.resize_for_scroll_area()

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
