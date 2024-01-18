from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import LeadStates
from .base_header_widget import HeaderWidget

if TYPE_CHECKING:
    from ....attr_box.lead_state_attr_box import LeadStateAttrBox


class LeadStateHeaderWidget(HeaderWidget):
    def __init__(self, attr_box: "LeadStateAttrBox", lead_state: LeadStates) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.lead_state = lead_state
        self.header_label = self._setup_header_label(self.lead_state.capitalize())
        self.separator = self.create_separator()
        self._setup_layout()

