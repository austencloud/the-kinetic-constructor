from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
from constants import COLOR, LEAD_STATE, MOTION_TYPE
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    MotionAttributes,
)
from widgets.attr_panel.base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import (
        ScrollArea,
    )

from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QHBoxLayout


class BaseFilterTab(QTabWidget):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.tabs: List[BaseAttrPanel] = []
        self.motion_type_attr_panel = None
        self.color_attr_panel = None
        self.lead_state_attr_panel = None
        self.letter_type: LetterTypeNums = letter_type
        self.setup_ui()

    def setup_ui(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_tabs(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) == -1:
                self.addTab(self.motion_type_attr_panel, "Filter by Motion Type")
            elif tab == COLOR and self.indexOf(self.color_attr_panel) == -1:
                self.addTab(self.color_attr_panel, "Filter by Colors")
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) == -1:
                self.addTab(self.lead_state_attr_panel, "Filter by Lead State")

    def hide_tabs(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) != -1:
                self.removeTab(self.indexOf(self.motion_type_attr_panel))
            elif tab == COLOR and self.indexOf(self.color_attr_panel) != -1:
                self.removeTab(self.indexOf(self.color_attr_panel))
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) != -1:
                self.removeTab(self.indexOf(self.lead_state_attr_panel))

    def bring_to_front(self, tab: MotionAttributes) -> None:
        if tab == MOTION_TYPE:
            index = self.indexOf(self.motion_type_attr_panel)
        elif tab == COLOR:
            index = self.indexOf(self.color_attr_panel)
        elif tab == LEAD_STATE:
            index = self.indexOf(self.lead_state_attr_panel)
        if index != -1:
            self.setCurrentIndex(index)

    def resize_filter_tab(self) -> None:
        for tab in self.tabs:
            tab.resize_attr_panel()

    def show_panels_based_on_chosen_letters(self) -> None:
        # implement in subclass
        pass 
    