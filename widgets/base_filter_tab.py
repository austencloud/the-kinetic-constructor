from multiprocessing import parent_process
from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QTabWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_panel import IGColorAttrPanel
from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_panel import (
    IGMotionTypeAttrPanel,
)

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
