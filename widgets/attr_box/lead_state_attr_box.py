from typing import TYPE_CHECKING
from constants import LEAD_STATE
from utilities.TypeChecking.TypeChecking import LeadStates, LeadStates
from widgets.header_widget import HeaderWidget

from .base_attr_box import AttrBox
from .attr_box_widgets.turns_widget.lead_state_turns_widget import LeadStateTurnsWidget

if TYPE_CHECKING:
    from ..attr_panel.lead_state_attr_panel import LeadStateAttrPanel


class LeadStateAttrBox(AttrBox):
    def __init__(
        self, attr_panel: "LeadStateAttrPanel", lead_state: LeadStates
    ) -> None:
        super().__init__(attr_panel, None)
        self.lead_state = lead_state
        self.attribute_type = LEAD_STATE
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        self.header_widget = HeaderWidget(self)
        self.turns_widget = LeadStateTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
