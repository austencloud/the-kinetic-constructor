from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from widgets.filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns
from constants import *
from widgets.graph_editor_tab.attr_panel.attr_panel import AttrPanel

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab


class IGFilterFrame(FilterFrame):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.apply_filters()
        self.connect_filter_buttons()
        self.attr_panel = AttrPanel(ig_tab, "ig_tab")
        self.layout.addWidget(self.attr_panel)
    # Overrides and additional methods specific to IGFilterFrame
    def apply_filters(self):
        super().apply_filters()
        # Specific logic for IGTab
        # ...

    def connect_filter_buttons(self):
        super().connect_filter_buttons()
        # Specific logic for IGTab
        # ...
        
