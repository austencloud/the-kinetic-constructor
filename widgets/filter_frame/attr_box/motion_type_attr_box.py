from typing import TYPE_CHECKING, Dict, List
from constants import DASH, MOTION_TYPE, OPP, SAME, STATIC
from utilities.TypeChecking.TypeChecking import MotionTypes
from objects.motion.motion import Motion
from .attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget
from .attr_box_widgets.turns_widgets.motion_type_turns_widget import (
    MotionTypeTurnsWidget,
)
from .base_attr_box import BaseAttrBox
from ...attr_box_widgets.header_widgets.motion_type_header_widget import (
    IGMotionTypeHeaderWidget,
)

if TYPE_CHECKING:
    from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QSizePolicy


class MotionTypeAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "MotionTypeAttrPanel",
        pictographs: List["Pictograph"],
        motion_type: MotionTypes,
    ) -> None:
        super().__init__(attr_panel, None)
        self.attr_panel = attr_panel
        self.motion_type = motion_type
        self.pictographs: Dict[str, Pictograph] = pictographs
        self.font_size = self.width() // 10
        self.widgets: List[BaseAttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}
        self.setLayout(self.vbox_layout)
        self._setup_widgets()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.setSpacing(0)
        self.adjustSize()
        self.attribute_type = MOTION_TYPE
        if self.motion_type in [DASH, STATIC]:
            self.same_button = self.header_widget.same_button
            self.opp_button = self.header_widget.opp_button
            self.same_opp_buttons = [self.same_button, self.opp_button]
            self.vtg_dir_btn_state = {SAME: False, OPP: False}

    def _setup_widgets(self) -> None:
        self.header_widget = IGMotionTypeHeaderWidget(self, self.motion_type)
        self.turns_widget = MotionTypeTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)

    def resize_ig_motion_type_attr_box(self) -> None:
        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.pictographs.values())

    def update_attr_box(self, motion: Motion) -> None:
        self.turns_widget.turn_display_manager.update_turns_display(motion.turns)