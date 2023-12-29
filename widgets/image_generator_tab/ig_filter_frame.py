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
        self.ig_tab.ig_scroll_area.apply_turn_filters(self.filters)
        
    def apply_filters(self) -> None:
        selected_blue_turns = self.comboboxes[BLUE_TURNS].currentText()
        selected_red_turns = self.comboboxes[RED_TURNS].currentText()
        selected_left_end_or = self.comboboxes[BLUE_END_OR].currentText()
        selected_right_end_or = self.comboboxes[RED_END_OR].currentText()

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            "blue_turns": selected_blue_turns,
            "red_turns": selected_red_turns,
            "left_end_or": selected_left_end_or,
            "right_end_or": selected_right_end_or,
        }

        self.ig_tab.ig_scroll_area.apply_turn_filters(self.filters)
