from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from constants import COLOR, LEAD_STATE, MOTION_TYPE, OPP, SAME
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LeadStates,
    MotionAttributes,
    MotionTypes,
)
from widgets.attr_box.attr_box_widgets.turns_widget.color_turns_widget import (
    ColorTurnsWidget,
)
from widgets.attr_box.attr_box_widgets.turns_widget.lead_state_turns_widget import (
    LeadStateTurnsWidget,
)
from widgets.attr_box.attr_box_widgets.turns_widget.motion_type_turns_widget import (
    MotionTypeTurnsWidget,
)
from widgets.attr_box.rot_dir_button_manager import RotDirButtonManager
from widgets.header_widget import HeaderWidget
from .attr_box_widgets.turns_widget.base_turns_widget.base_turns_widget import (
    TurnsWidget,
)
from .attr_box_widgets.base_attr_box_widget import AttrBoxWidget

if TYPE_CHECKING:
    from ..attr_panel import AttrPanel


class AttrBox(QFrame):
    def __init__(
        self,
        attr_panel,
        attribute_type: MotionAttributes,
        attribute: Union[MotionAttributes, Colors, LeadStates] = None,
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel: "AttrPanel" = attr_panel
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.turns_widget: TurnsWidget = None
        self.turn_display_border = 2
        self.attr_box_border_width = 0
        self.pixmap_cache: Dict[str, QPixmap] = {}
        self.vtg_dir_btn_state: Dict[str, bool] = {SAME: True, OPP: False}
        self.attribute_type: MotionAttributes = attribute_type
        if self.attribute_type == MOTION_TYPE:
            self.motion_type: MotionTypes = attribute
        elif self.attribute_type == COLOR:
            self.color: Colors = attribute
        elif self.attribute_type == LEAD_STATE:
            self.lead_state: LeadStates = attribute
        self._setup_widgets()
        self._setup_layouts()

    def _setup_widgets(self) -> None:
        if self.attribute_type == MOTION_TYPE:
            self.rot_dir_button_manager = RotDirButtonManager(self)
            self.turns_widget = MotionTypeTurnsWidget(self)
        elif self.attribute_type == COLOR:
            self.turns_widget = ColorTurnsWidget(self)
        elif self.attribute_type == LEAD_STATE:
            self.turns_widget = LeadStateTurnsWidget(self)
        self.header_widget = HeaderWidget(self)

    def _setup_layouts(self) -> None:
        self.vbox_layout = QVBoxLayout(self)
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vbox_layout.setSpacing(0)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(
            f"#AttributeBox {{ "
            f"border: {self.attr_box_border_width}px solid {color_hex};"
            f" border-style: inset; "
            f"}}"
        )

    ### CREATE LABELS ###

    def resize_attr_box(self) -> None:
        self.turns_widget.resize_turns_widget()
