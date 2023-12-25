from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from constants.constants import (
    BLUE_END_ORIENTATION,
    BLUE_TURNS,
    RED_END_ORIENTATION,
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

        self.left_end_orientation_combobox.currentTextChanged.connect(
            self.apply_filters
        )

        self.connect_filter_boxes()

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
        selected_left_end_orientation = self.left_end_orientation_combobox.currentText()
        selected_right_end_orientation = (
            self.right_end_orientation_combobox.currentText()
        )

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            BLUE_TURNS: selected_blue_turns,
            RED_TURNS: selected_red_turns,
            BLUE_END_ORIENTATION: selected_left_end_orientation,
            RED_END_ORIENTATION: selected_right_end_orientation,
        }

        self.option_picker_tab.scroll_area.apply_turn_filters(self.filters)
