from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.ig_tab.ig_tab import IGTab


class BaseFilterTab(QTabWidget):
    def __init__(self, parent_tab: Union["IGTab", "OptionPickerTab"]) -> None:
        super().__init__(parent_tab)
        self.ig_tab = parent_tab
        self.parent_tab = parent_tab
        self.attr_panel = None

    def apply_filters(self) -> None:
        pass

    def connect_filter_buttons(self) -> None:
        pass
