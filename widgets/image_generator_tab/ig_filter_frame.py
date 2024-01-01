from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from widgets.filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns
from constants import *

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab


class IGFilterFrame(FilterFrame):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.apply_filters()
        self.connect_filter_buttons()

    # Overrides and additional methods specific to IGFilterFrame
    def apply_filters(self):
        super().apply_filters()
        # Specific logic for IGTab
        # ...

    def connect_filter_buttons(self):
        super().connect_filter_buttons()
        # Specific logic for IGTab
        # ...
        
