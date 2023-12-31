from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from constants import (
    BLUE_END_ORI,
    BLUE_START_ORI,
    BLUE_TURNS,
    RED_END_ORI,
    RED_START_ORI,
    RED_TURNS,
)
from widgets.filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab


class OptionPickerFilterFrame(FilterFrame):
    def __init__(self, option_picker_tab: "OptionPickerTab") -> None:
        super().__init__(option_picker_tab)
        self.option_picker_tab = option_picker_tab
        self.apply_filters()
        self.connect_filter_boxes()

    def apply_filters(self) -> None:
        selected_blue_turns = self.comboboxes[BLUE_TURNS].currentText()
        selected_red_turns = self.comboboxes[RED_TURNS].currentText()
        selected_left_start_or = self.comboboxes[BLUE_START_ORI].currentText()
        selected_right_start_or = self.comboboxes[RED_START_ORI].currentText()
        selected_blue_end_or = self.comboboxes[BLUE_END_ORI].currentText()
        selected_red_end_or = self.comboboxes[RED_END_ORI].currentText()

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            BLUE_TURNS: selected_blue_turns,
            RED_TURNS: selected_red_turns,
            BLUE_START_ORI: selected_left_start_or,
            RED_START_ORI: selected_right_start_or,
            BLUE_END_ORI: selected_blue_end_or,
            RED_END_ORI: selected_red_end_or,
        }
