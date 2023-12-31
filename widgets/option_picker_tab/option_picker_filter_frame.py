from typing import TYPE_CHECKING, Union, Dict
from Enums import Orientation, Turns
from widgets.filter_frame import FilterFrame
from constants import *

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab


class OptionPickerFilterFrame(FilterFrame):
    def __init__(self, option_picker_tab: "OptionPickerTab") -> None:
        super().__init__(option_picker_tab)
        self.option_picker_tab = option_picker_tab
        self.apply_filters()
        self.connect_filter_buttons()

    def apply_filters(self) -> None:
        selected_blue_turns = self.get_selected_button_value(BLUE_TURNS)
        selected_red_turns = self.get_selected_button_value(RED_TURNS)
        selected_blue_start_ori = self.get_selected_button_value(BLUE_START_ORI)
        selected_red_start_ori = self.get_selected_button_value(RED_START_ORI)
        selected_blue_end_ori = self.get_selected_button_value(BLUE_END_ORI)
        selected_red_end_ori = self.get_selected_button_value(RED_END_ORI)

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            BLUE_TURNS: selected_blue_turns,
            RED_TURNS: selected_red_turns,
            BLUE_START_ORI: selected_blue_start_ori,
            RED_START_ORI: selected_red_start_ori,
            BLUE_END_ORI: selected_blue_end_ori,
            RED_END_ORI: selected_red_end_ori,
        }

        # Call the method in OptionPickerTab to apply these filters
        # self.option_picker_tab.apply_filters(self.filters)

    def get_selected_button_value(self, group_key) -> str:
        button_group = self.button_groups[group_key]
        checked_button = button_group.checkedButton()
        return checked_button.text() if checked_button else None

    def connect_filter_buttons(self):
        # Connect button group signals to apply_filters
        for group in self.button_groups.values():
            group.buttonClicked.connect(self.apply_filters)
