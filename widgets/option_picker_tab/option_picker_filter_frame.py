from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from constants import (
    BLUE_END_OR,
    BLUE_START_OR,
    BLUE_TURNS,
    RED_END_OR,
    RED_START_OR,
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
        self.option_picker_tab.scroll_area.apply_turn_filters(self.filters)

    def apply_filters(self) -> None:
        selected_blue_turns = [
            turn
            for turn, checkbox in self.blue_turn_checkboxes.items()
            if checkbox.isChecked()
        ][0]
        selected_red_turns = [
            turn
            for turn, checkbox in self.red_turn_checkboxes.items()
            if checkbox.isChecked()
        ][0]
        selected_left_end_or = self.left_end_or_combobox.currentText()
        selected_right_end_or = self.right_end_or_combobox.currentText()
        selected_left_start_or = self.left_start_or_combobox.currentText()
        selected_right_start_or = self.right_start_or_combobox.currentText()

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            BLUE_TURNS: selected_blue_turns,
            RED_TURNS: selected_red_turns,
            BLUE_START_OR: selected_left_start_or,
            RED_START_OR: selected_right_start_or,
            BLUE_END_OR: selected_left_end_or,
            RED_END_OR: selected_right_end_or,
        }
