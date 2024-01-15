from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from constants import LEAD_STATE
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import LeadStates, LeadStates
from .attr_box_widgets.prop_rot_dir_widgets.prop_rot_dir_widget import PropRotDirWidget

from .base_attr_box import BaseAttrBox
from .attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from .attr_box_widgets.header_widgets.lead_state_header_widget import (
    LeadStateHeaderWidget,
)
from .attr_box_widgets.turns_widgets.lead_state_turns_widget import LeadStateTurnsWidget

if TYPE_CHECKING:
    from ..attr_panel.lead_state_attr_panel import IGLeadStateAttrPanel
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout


class LeadStateAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "IGLeadStateAttrPanel",
        pictographs: List["Pictograph"],
        lead_state: LeadStates,
    ) -> None:
        super().__init__(attr_panel, None)  # Note the None for the single pictograph
        self.attr_panel = attr_panel
        self.lead_state = lead_state
        self.pictographs: Dict[str, Pictograph] = pictographs
        self.font_size = self.width() // 10
        self.widgets: List[BaseAttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.hbox_layout = QHBoxLayout()
        self.vbox2 = QVBoxLayout()
        self.layout: QHBoxLayout = self.hbox_layout
        self.hbox_layout.addLayout(self.vbox_layout)
        self._setup_widgets()
        self.attribute_type = LEAD_STATE

    def _setup_widgets(self) -> None:  # add common widgets
        self.header_widget = LeadStateHeaderWidget(self, self.lead_state)
        self.turns_widget = LeadStateTurnsWidget(self)
        self.prop_rot_dir_widget = PropRotDirWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
        self.hbox_layout.addWidget(self.prop_rot_dir_widget, 2)
        self.setLayout(self.hbox_layout)

    def resize_ig_lead_state_attr_box(self) -> None:
        self.setMinimumWidth(int(self.attr_panel.ig_tab.width() / 3))
        self.setMaximumWidth(int(self.attr_panel.ig_tab.width() / 3))
        self.turns_widget.resize_turns_widget()
        self.prop_rot_dir_widget.resize_prop_rot_dir_widget()

    def update_attr_box(self, motion: Motion) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                self.turns_widget._update_turnbox(motion.turns)

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.pictographs.values())