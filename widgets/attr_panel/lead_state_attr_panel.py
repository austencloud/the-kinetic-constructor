from constants import LEADING, TRAILING
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import LeadStates, Turns
from ..attr_box.lead_state_attr_box import LeadStateAttrBox
from .base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class LeadStateAttrPanel(BaseAttrPanel):
    def __init__(self, parent_tab: "IGTab") -> None:
        super().__init__(parent_tab)
        self._setup_boxes()
        self.setup_layouts()

    def _setup_boxes(self) -> None:
        self.leading_box = LeadStateAttrBox(self, LEADING)
        self.trailing_box = LeadStateAttrBox(self, TRAILING)
        self.boxes: List[LeadStateAttrBox] = [
            self.leading_box,
            self.trailing_box,
        ]

    def setup_layouts(self) -> None:
        super().setup_layouts()
        for box in self.boxes:
            self.layout.addWidget(box)
