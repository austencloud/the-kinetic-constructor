from typing import TYPE_CHECKING




if TYPE_CHECKING:
    from widgets.scroll_area.scroll_area import ScrollArea


class ScrollAreaUpdater:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area

    def update_pictographs(self) -> None:
        deselected_letters = (
            self.scroll_area.pictograph_factory.get_deselected_letters()
        )
        selected_letters = set(self.scroll_area.codex.selected_letters)

        if self._only_deselection_occurred(deselected_letters, selected_letters):
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(
                    letter
                )
        else:
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(
                    letter
                )
            self.scroll_area.pictograph_factory.process_selected_letters()
        self.scroll_area.display_manager.order_and_display_pictographs()

    def _only_deselection_occurred(self, deselected_letters, selected_letters) -> bool:
        if not deselected_letters:
            return False
        if not selected_letters:
            return True

        current_pictograph_letters = {
            key.split("_")[0] for key in self.scroll_area.pictographs
        }

        return (
            len(deselected_letters) > 0
            and len(selected_letters) == len(current_pictograph_letters) - 1
        )
