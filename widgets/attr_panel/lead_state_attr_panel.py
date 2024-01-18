from constants import LEAD_STATE, LEADING, TRAILING
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import LeadStates, Turns
from ..attr_box.attr_box import AttrBox
from .base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab
    from widgets.ig_tab.ig_tab import IGTab


class LeadStateAttrPanel(BaseAttrPanel):
    def __init__(self, filter_tab: "FilterTab") -> None:
        super().__init__(filter_tab)
        self._setup_boxes()
        self.setup_layouts()

    def _setup_boxes(self) -> None:
        self.leading_box = AttrBox(self, LEAD_STATE, LEADING)
        self.trailing_box = AttrBox(self, LEAD_STATE, TRAILING)
        self.boxes: List[AttrBox] = [
            self.leading_box,
            self.trailing_box,
        ]

    def setup_layouts(self) -> None:
        super().setup_layouts()
        for box in self.boxes:
            self.layout.addWidget(box)
