from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from widgets.filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns
from constants import *

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab


class IGFilterFrame(FilterFrame):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.apply_filters()
        self.connect_filter_boxes()

    def apply_filters(self) -> None:
        selected_blue_start_ori = self.comboboxes[BLUE_START_ORI].currentText()
        selected_blue_end_ori = self.comboboxes[BLUE_END_ORI].currentText()
        selected_blue_turns = self.comboboxes[BLUE_TURNS].currentText()

        selected_red_start_ori = self.comboboxes[BLUE_END_ORI].currentText()
        selected_red_end_ori = self.comboboxes[RED_END_ORI].currentText()
        selected_red_turns = self.comboboxes[RED_TURNS].currentText()

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            BLUE_START_ORI: selected_blue_start_ori,
            BLUE_END_ORI: selected_blue_end_ori,
            BLUE_TURNS: selected_blue_turns,
            RED_START_ORI: selected_red_start_ori,
            RED_END_ORI: selected_red_end_ori,
            RED_TURNS: selected_red_turns,
        }

        self.ig_tab.ig_scroll_area.apply_filters(self.filters)
