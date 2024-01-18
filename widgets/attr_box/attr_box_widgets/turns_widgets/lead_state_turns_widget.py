from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, List, Union
from constants import (
    BLUE,
    ICON_DIR,
    RED,
)
from objects.motion.motion import Motion
from widgets.attr_box.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
    TurnsWidget,
)

if TYPE_CHECKING:
    from widgets.attr_box.lead_state_attr_box import LeadStateAttrBox


class LeadStateTurnsWidget(TurnsWidget):
    def __init__(self, attr_box: "LeadStateAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: LeadStateAttrBox = attr_box
