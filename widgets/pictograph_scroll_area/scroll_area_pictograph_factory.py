from typing import TYPE_CHECKING, Dict, List, Literal, Set
from constants import IG_PICTOGRAPH, OPTION
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.Letters import Letters_list
from utilities.TypeChecking.TypeChecking import Letters
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.pictograph_scroll_area import (
        PictographScrollArea,
    )
from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    END_POS,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    START_POS,
)


class ScrollAreaPictographFactory:
    def __init__(self, scroll_area: "PictographScrollArea") -> None:
        self.pictographs: Dict[Letters, IGPictograph] = {}
        self.scroll_area = scroll_area

    def process_selected_letters(self) -> None:
        sorted_selected_letters = self.get_sorted_selected_letters()
        for letter in sorted_selected_letters:
            self.process_letter(letter)

    def get_sorted_selected_letters(self) -> List[Letters]:
        return sorted(
            self.scroll_area.parent_tab.selected_letters,
            key=lambda x: Letters_list.index(x),
        )

    def process_letter(self, letter) -> None:
        pictograph_dicts = self.scroll_area.letters.get(letter, [])
        for pictograph_dict in self.scroll_area.filter_frame_manager.filter_pictographs(
            pictograph_dicts
        ):
            self.create_or_update_pictograph(pictograph_dict.copy(), letter)

    def create_or_update_pictograph(self, pictograph_dict, letter) -> None:
        pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
        ig_pictograph = self.get_or_create_pictograph(pictograph_key)
        self.update_pictograph_from_attr_panel(ig_pictograph, pictograph_dict)
        ig_pictograph.update_pictograph(pictograph_dict)

    def update_pictograph_from_attr_panel(
        self, ig_pictograph: Pictograph, pictograph_dict
    ) -> None:
        for motion in ig_pictograph.motions.values():
            motion.attr_manager.update_motion_attributes_from_filter_tab(
                self.scroll_area.parent_tab.filter_tab, pictograph_dict
            )

    def get_deselected_letters(self) -> Set[Letters]:
        selected_letters = set(self.scroll_area.parent_tab.selected_letters)
        existing_letters = {key.split("_")[0] for key in self.pictographs.keys()}
        return existing_letters - selected_letters

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key for key in self.pictographs if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            ig_pictograph = self.pictographs.pop(key)
            self.scroll_area.layout.removeWidget(ig_pictograph.view)
            ig_pictograph.view.setParent(None)
            ig_pictograph.view.deleteLater()

    def get_or_create_pictograph(self, pictograph_key) -> IGPictograph:
        if pictograph_key not in self.pictographs:
            self.pictographs[pictograph_key] = self._create_pictograph(IG_PICTOGRAPH)
        return self.pictographs[pictograph_key]

    def _create_pictograph(
        self,
        graph_type: Literal["option", "ig_pictograph"],
    ) -> Option | IGPictograph:
        if graph_type == OPTION:
            pictograph = Option(self.scroll_area.main_widget, self)
        elif graph_type == IG_PICTOGRAPH:
            pictograph = IGPictograph(self.scroll_area.main_widget, self)
        return pictograph

    def generate_pictograph_key_from_dict(self, pictograph_dict) -> str:
        return (
            f"{pictograph_dict[LETTER]}_"
            f"{pictograph_dict[START_POS]}→{pictograph_dict[END_POS]}_"
            f"{pictograph_dict[BLUE_MOTION_TYPE]}_"
            f"{pictograph_dict[BLUE_PROP_ROT_DIR]}_"
            f"{pictograph_dict[BLUE_START_LOC]}→{pictograph_dict[BLUE_END_LOC]}_"
            f"{pictograph_dict[RED_MOTION_TYPE]}_"
            f"{pictograph_dict[RED_PROP_ROT_DIR]}_"
            f"{pictograph_dict[RED_START_LOC]}→{pictograph_dict[RED_END_LOC]}"
        )
