from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QTabWidget

from widgets.filter_frame.attr_panel.color_attr_panel import ColorAttrPanel

if TYPE_CHECKING:
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from widgets.ig_tab.ig_tab import IGTab

from typing import TYPE_CHECKING, List
from ..attr_panel.lead_state_attr_panel import IGLeadStateAttrPanel
from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
from PyQt6.QtWidgets import QHBoxLayout


class FilterTab(QTabWidget):
    def __init__(self, parent_tab: Union["IGTab", "OptionPickerTab"]) -> None:
        super().__init__(parent_tab)
        self.parent_tab = parent_tab
        self.parent_tab = parent_tab
        self.attr_panel = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.motion_type_attr_panel = MotionTypeAttrPanel(self.parent_tab)
        self.color_attr_panel = ColorAttrPanel(self.parent_tab)
        self.lead_state_attr_panel = IGLeadStateAttrPanel(self.parent_tab)
        self.addTab(self.motion_type_attr_panel, "Filter by Motion Type")
        self.addTab(self.color_attr_panel, "Filter by Colors")
        self.addTab(self.lead_state_attr_panel, "Filter by Lead State")
        self.panels: List[
            MotionTypeAttrPanel | ColorAttrPanel | IGLeadStateAttrPanel
        ] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]
        self.currentChanged.connect(self.parent_tab.resize_tab)
        if self.lead_state_attr_panel.isVisible():
            self.currentChanged.connect(self.lead_state_attr_panel.reset_turns)
        elif self.motion_type_attr_panel.isVisible():
            self.currentChanged.connect(self.motion_type_attr_panel.reset_turns)
        elif self.color_attr_panel.isVisible():
            self.currentChanged.connect(self.color_attr_panel.reset_turns)

        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
