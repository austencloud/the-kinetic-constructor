from typing import TYPE_CHECKING
from widgets.base_filter_tab import BaseFilterTab

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab


class OptionPickerFilterTab(BaseFilterTab):
    def __init__(self, option_picker_tab: "OptionPickerTab") -> None:
        super().__init__(option_picker_tab)
        self.option_picker_tab = option_picker_tab
        self.apply_filters()
        self.connect_filter_buttons()
