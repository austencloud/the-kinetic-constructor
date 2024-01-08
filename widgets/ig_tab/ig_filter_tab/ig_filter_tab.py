from multiprocessing import parent_process
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
from widgets.base_filter_tab import BaseFilterTab
from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_panel import IGColorAttrPanel
from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_panel import IGLeadStateAttrPanel
from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_panel import (
    IGMotionTypeAttrPanel,
)

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGFilterTab(BaseFilterTab):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.motion_attr_panel = IGMotionTypeAttrPanel(self.ig_tab)
        self.color_attr_panel = IGColorAttrPanel(self.ig_tab)
        self.lead_state_attr_panel = IGLeadStateAttrPanel(self.ig_tab)
        self.addTab(self.motion_attr_panel, "Filter by Motion Type")
        self.addTab(self.lead_state_attr_panel, "Filter by Lead State")
        self.addTab(self.color_attr_panel, "Filter by Colors")
        self.currentChanged.connect(self.ig_tab.resize_ig_tab)
        self.currentChanged.connect(self.ig_tab.ig_scroll_area.reset_turns)
        self.currentChanged.connect(self.motion_attr_panel.reset_turns)
        self.currentChanged.connect(self.color_attr_panel.reset_turns)
