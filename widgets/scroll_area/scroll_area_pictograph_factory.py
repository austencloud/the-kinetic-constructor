from typing import TYPE_CHECKING, Literal, Set
from constants import IG_PICTOGRAPH, OPTION
from utilities.TypeChecking.TypeChecking import Letters
from widgets.ig_tab.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea

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
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area

    def get_or_create_pictograph(
        self, pictograph_key: str, pictograph_dict=None
    ) -> IGPictograph:
        if (
            pictograph_key
            in self.scroll_area.main_widget.all_pictographs[
                pictograph_key.split("_")[0]
            ]
        ):
            return self.scroll_area.main_widget.all_pictographs[
                pictograph_key.split("_")[0]
            ][pictograph_key]
        elif pictograph_dict is not None:
            ig_pictograph = self.create_pictograph(IG_PICTOGRAPH)
            ig_pictograph.state_updater.update_pictograph(pictograph_dict)
            self.scroll_area.main_widget.all_pictographs[pictograph_key.split("_")[0]][
                pictograph_key
            ] = ig_pictograph
            return ig_pictograph
        else:
            raise ValueError(
                "Pictograph dict is required for creating a new pictograph."
            )

    def process_selected_letters(self) -> None:
        selected_letters = set(self.scroll_area.parent_tab.selected_letters)
        for letter in selected_letters:
            if letter not in self.scroll_area.main_widget.all_pictographs:
                pictograph_dicts = self.scroll_area.letters.get(letter, [])
                for pictograph_dict in pictograph_dicts:
                    pictograph_key = self.generate_pictograph_key_from_dict(
                        pictograph_dict
                    )
                    self.get_or_create_pictograph(pictograph_key, pictograph_dict)
            for (
                pictograph_key,
                pictograph,
            ) in self.scroll_area.main_widget.all_pictographs.get(letter, {}).items():
                self.scroll_area.pictographs[pictograph_key] = pictograph

    def get_deselected_letters(self) -> Set[Letters]:
        selected_letters = set(self.scroll_area.parent_tab.selected_letters)
        existing_letters = {
            key.split("_")[0] for key in self.scroll_area.pictographs.keys()
        }
        return existing_letters - selected_letters

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.scroll_area.pictographs
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            ig_pictograph = self.scroll_area.pictographs.pop(key)
            scroll_section = self.scroll_area.section_manager.get_section(
                ig_pictograph.letter_type
            )
            scroll_section.remove_pictograph(ig_pictograph)

    def get_pictograph(self, pictograph_key) -> IGPictograph:
        return self.scroll_area.pictographs[pictograph_key]

    def create_pictograph(
        self,
        graph_type: Literal["option", "ig_pictograph"],
    ) -> Option | IGPictograph:
        if graph_type == OPTION:
            pictograph = Option(
                self.scroll_area.main_widget,
                self.scroll_area,
            )
        elif graph_type == IG_PICTOGRAPH:
            pictograph = IGPictograph(
                self.scroll_area.main_widget,
                self.scroll_area,
            )
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
