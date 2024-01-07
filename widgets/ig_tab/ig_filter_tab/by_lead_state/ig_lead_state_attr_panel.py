from constants import BLUE, RED
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import LeadStates, Turns
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import IGLeadStateAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGLeadStateAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.blue_attr_box = IGLeadStateAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, BLUE
        )
        self.red_attr_box = IGLeadStateAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, RED
        )
        self.boxes: List[IGLeadStateAttrBox] = [
            self.blue_attr_box,
            self.red_attr_box,
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
                if box.turns_widget.turnbox.currentText() in ["0", "1", "2", "3"]:
                    return int(box.turns_widget.turnbox.currentText())
                elif box.turns_widget.turnbox.currentText() in ["0.5", "1.5", "2.5"]:
                    return float(box.turns_widget.turnbox.currentText())


    def resize_ig_lead_state_attr_panel(self) -> None:
        self.layout.setSpacing(int(self.blue_attr_box.width() / 5))
        for box in self.boxes:
            box.resize_ig_lead_state_attr_box()

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turnbox.setCurrentText("0")
            