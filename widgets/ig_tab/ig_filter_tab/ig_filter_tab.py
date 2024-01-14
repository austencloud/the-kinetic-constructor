from typing import TYPE_CHECKING, List
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.base_filter_tab import BaseFilterTab
from .by_color.ig_color_attr_panel import IGColorAttrPanel
from .by_lead_state.ig_lead_state_attr_panel import IGLeadStateAttrPanel
from .by_motion_type.ig_motion_type_attr_panel import IGMotionTypeAttrPanel
from PyQt6.QtWidgets import QHBoxLayout

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
        self.addTab(self.color_attr_panel, "Filter by Colors")
        self.addTab(self.lead_state_attr_panel, "Filter by Lead State")
        self.panels: List[
            IGMotionTypeAttrPanel | IGColorAttrPanel | IGLeadStateAttrPanel
        ] = [
            self.motion_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]
        self.currentChanged.connect(self.ig_tab.resize_ig_tab)
        self.currentChanged.connect(self.ig_tab.ig_scroll_area.reset_turns)
        self.currentChanged.connect(self.motion_attr_panel.reset_turns)
        self.currentChanged.connect(self.color_attr_panel.reset_turns)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
