from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QCheckBox, QVBoxLayout
from constants.string_constants import CLOCK, COUNTER, IN, OUT
from filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Orientations, Turns
from PyQt6.QtWidgets import QComboBox

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
        ][0]  # Access the first element of the list
        selected_red_turns = [
            turn
            for turn, checkbox in self.red_turn_checkboxes.items()
            if checkbox.isChecked()
        ][0]  # Access the first element of the list
        selected_left_end_orientation = self.left_end_orientation_combobox.currentText()
        selected_right_end_orientation = self.right_end_orientation_combobox.currentText()

        self.filters: Dict[str, Union[Turns, Orientations]] = {
            "left_turns": selected_blue_turns,
            "right_turns": selected_red_turns,
            "left_end_orientation": selected_left_end_orientation,
            "right_end_orientation": selected_right_end_orientation,
        }

        self.option_picker_tab.scroll_area.apply_turn_filters(self.filters)
