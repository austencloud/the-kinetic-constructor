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


