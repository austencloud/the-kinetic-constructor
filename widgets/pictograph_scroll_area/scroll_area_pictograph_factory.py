from typing import TYPE_CHECKING, Dict, List, Literal, Set
from constants import IG_PICTOGRAPH, OPTION
from objects.pictograph.pictograph import Pictograph
from objects.pictograph.pictograph_loader import PictographLoader
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Letters
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.option_picker_tab.option import Option

if TYPE_CHECKING:
    from .scroll_area import ScrollArea
    from widgets.main_widget import MainWidget

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


class PictographFactory:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget

    def create_all_pictographs(self) -> None:
        for letter in all_letters:
            pictograph_dicts = self.main_widget.ig_tab.scroll_area.letters.get(
                letter, []
            )
            for pictograph_dict in pictograph_dicts:
                pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
                if pictograph_key not in self.main_widget.all_pictographs:
                    self.main_widget.all_pictographs[
                        pictograph_key
                    ] = self.create_pictograph(IG_PICTOGRAPH)
                    self.main_widget.all_pictographs[
                        pictograph_key
                    ].state_updater.update_pictograph(pictograph_dict)

    def process_selected_letters(self) -> None:
        selected_letters = set(
            self.main_widget.ig_tab.scroll_area.parent_tab.selected_letters
        )
        for pictograph_key, ig_pictograph in self.main_widget.all_pictographs.items():
            letter = pictograph_key.split("_")[0]
            if letter in selected_letters:
                self.main_widget.pictograph_loader.pictograph_ready.connect(
                    self.main_widget.handle_pictograph_ready(pictograph_key)
                )
                self.main_widget.pictograph_loader.prioritize_pictograph(pictograph_key)
                # ig_pictograph.show()
            # else:
            #     ig_pictograph.hide()

    def get_sorted_selected_letters(self) -> List[Letters]:
        return sorted(
            self.main_widget.ig_tab.scroll_area.parent_tab.selected_letters,
            key=lambda x: all_letters.index(x),
        )

    def process_letter(self, letter) -> None:
        pictograph_dicts = self.main_widget.ig_tab.scroll_area.letters.get(letter, [])
        for (
            pictograph_dict
        ) in self.main_widget.ig_tab.scroll_area.filter_tab_manager.filter_pictographs(
            pictograph_dicts
        ):
            pictograph_key = self.generate_pictograph_key_from_dict(pictograph_dict)
            ig_pictograph = self.get_pictograph(pictograph_key)
            ig_pictograph.state_updater.update_pictograph(pictograph_dict)



    def get_deselected_letters(self) -> Set[Letters]:
        selected_letters = set(
            self.main_widget.ig_tab.scroll_area.parent_tab.selected_letters
        )
        existing_letters = {
            key.split("_")[0]
            for key in self.main_widget.ig_tab.scroll_area.pictographs.keys()
        }
        return existing_letters - selected_letters

    def remove_deselected_letter_pictographs(self, deselected_letter) -> None:
        keys_to_remove = [
            key
            for key in self.main_widget.ig_tab.scroll_area.pictographs
            if key.startswith(deselected_letter + "_")
        ]
        for key in keys_to_remove:
            ig_pictograph = self.main_widget.ig_tab.scroll_area.pictographs.pop(key)
            scroll_section = (
                self.main_widget.ig_tab.scroll_area.section_manager.get_section(
                    ig_pictograph.letter_type
                )
            )
            scroll_section.remove_pictograph(ig_pictograph)

    def get_pictograph(self, pictograph_key) -> IGPictograph:
        return self.main_widget.ig_tab.scroll_area.pictographs[pictograph_key]

    def create_pictograph(
        self,
        graph_type: Literal["option", "ig_pictograph"],
    ) -> Option | IGPictograph:
        if graph_type == OPTION:
            pictograph = Option(
                self.main_widget.ig_tab.scroll_area.main_widget,
                self.main_widget.ig_tab.scroll_area,
            )
        elif graph_type == IG_PICTOGRAPH:
            pictograph = IGPictograph(
                self.main_widget.ig_tab.scroll_area.main_widget,
                self.main_widget.ig_tab.scroll_area,
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
