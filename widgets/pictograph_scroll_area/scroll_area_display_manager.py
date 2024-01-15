from typing import TYPE_CHECKING, Dict, List
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import (
    Letters,
)
from ..ig_tab.ig_scroll.ig_pictograph import IGPictograph

if TYPE_CHECKING:
    from .pictograph_scroll_area import PictographScrollArea


class ScrollAreaDisplayManager:
    COLUMN_COUNT = 6
    SPACING = 10

    def __init__(self, scroll_area: "PictographScrollArea") -> None:
        self.scroll_area = scroll_area

    def order_and_display_pictographs(self) -> None:
        ordered_pictographs = self.get_ordered_pictographs()
        self.clear_layout()
        for index, (key, ig_pictograph) in enumerate(ordered_pictographs.items()):
            self.add_pictograph_to_layout(ig_pictograph, index)

    def get_ordered_pictographs(self) -> Dict[Letters, IGPictograph]:
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

    def add_pictograph_to_layout(self, ig_pictograph: IGPictograph, index: int) -> None:
        row = index // self.COLUMN_COUNT
        col = index % self.COLUMN_COUNT
        self.scroll_area.layout.addWidget(ig_pictograph.view, row, col)
        ig_pictograph.view.resize_for_scroll_area()

    def remove_pictograph(
        self, pictograph_key: str, pictographs: Dict[Letters, IGPictograph]
    ) -> None:
        ig_pictograph: Pictograph = pictographs.pop(pictograph_key, None)
        if ig_pictograph:
            self.scroll_area.layout.removeWidget(ig_pictograph.view)
            ig_pictograph.view.setParent(None)
            ig_pictograph.view.deleteLater()

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
            letter.split("_")[0]
            for letter in self.scroll_area.parent_tab.selected_letters
        }
        return [
            key
            for key in self.scroll_area.pictographs
            if key.split("_")[0] not in selected_letters
        ]

    def get_ordered_pictographs(self) -> Dict[Letters, IGPictograph]:
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