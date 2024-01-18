from typing import TYPE_CHECKING
from constants import LEAD_STATE
from utilities.TypeChecking.TypeChecking import LeadStates, LeadStates

from .base_attr_box import BaseAttrBox
from .attr_box_widgets.header_widgets.lead_state_header_widget import (
    LeadStateHeaderWidget,
)
from .attr_box_widgets.turns_widgets.lead_state_turns_widget import LeadStateTurnsWidget

if TYPE_CHECKING:
    from ..attr_panel.lead_state_attr_panel import LeadStateAttrPanel


class LeadStateAttrBox(BaseAttrBox):
    def __init__(
        self, attr_panel: "LeadStateAttrPanel", lead_state: LeadStates
    ) -> None:
        super().__init__(attr_panel, None)
        self.lead_state = lead_state
        self.attribute_type = LEAD_STATE
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        self.header_widget = LeadStateHeaderWidget(self, self.lead_state)
        self.turns_widget = LeadStateTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
