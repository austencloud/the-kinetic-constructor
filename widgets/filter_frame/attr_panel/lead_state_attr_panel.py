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
        self.scroll_area = parent_tab
        self.leading_box = LeadStateAttrBox(self, LEADING)
        self.trailing_box = LeadStateAttrBox(self, TRAILING)
        self.boxes: List[LeadStateAttrBox] = [
            self.leading_box,
            self.trailing_box,
        ]

        self.setup_layouts()

    def setup_layouts(self) -> None:
        super().setup_layouts()
        for box in self.boxes:
            self.layout.addWidget(box)
        self.layout

    def get_turns_for_lead_state(self, lead_state: LeadStates) -> Turns:
        for box in self.boxes:
            if box.lead_state == lead_state:
                if box.turns_widget.turn_display_manager.turns_display.text() in [
                    "0",
                    "1",
                    "2",
                    "3",
                ]:
                    return int(
                        box.turns_widget.turn_display_manager.turns_display.text()
                    )
                elif box.turns_widget.turn_display_manager.turns_display.text() in [
                    "0.5",
                    "1.5",
                    "2.5",
                ]:
                    return float(
                        box.turns_widget.turn_display_manager.turns_display.text()
                    )

    def resize_attr_panel(self) -> None:
        self.layout.setSpacing(int(self.boxes[0].width() / 5))
        for box in self.boxes:
            box.resize_attr_box()
