from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from constants import BLUE, COLOR, LEAD_STATE, MOTION_TYPE, OPP, RED, SAME
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LeadStates,
    MotionAttributes,
    MotionTypes,
)

from .attr_box_widgets.rot_dir_button_manager import RotDirButtonManager
from widgets.header_widget import HeaderWidget
from .attr_box_widgets.turns_widget.turns_widget import (
    TurnsWidget,
)
from .attr_box_widgets.base_attr_box_widget import AttrBoxWidget
from PyQt6.QtWidgets import QSizePolicy

if TYPE_CHECKING:
    from ..attr_panel import AttrPanel


class AttrBox(QFrame):
    turns_widget: TurnsWidget

    def __init__(
        self,
        attr_panel,
        attribute_type: MotionAttributes,
        attribute: Union[MotionAttributes, Colors, LeadStates],
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel: "AttrPanel" = attr_panel
        self.font_size = self.attr_panel.width() // 20
        self.turn_display_border = 2
        self.vtg_dir_btn_state: Dict[str, bool] = {SAME: True, OPP: False}
        self._setup_attribute_type(attribute_type, attribute)
        self._setup_widgets()
        self._setup_layouts()

    def _setup_attribute_type(self, attribute_type, attribute) -> None:
        self.attribute_type: MotionAttributes = attribute_type
        if self.attribute_type == MOTION_TYPE:
            self.motion_type: MotionTypes = attribute
        elif self.attribute_type == COLOR:
            self.color: Colors = attribute
        elif self.attribute_type == LEAD_STATE:
            self.lead_state: LeadStates = attribute

    def _setup_widgets(self) -> None:
        self.rot_dir_button_manager = RotDirButtonManager(self)
        self.header_widget = HeaderWidget(self)
        self.turns_widget = TurnsWidget(self)

        if self.attribute_type == COLOR:
            if self.color == RED:
                self.apply_border_style("#ED1C24")
            elif self.color == BLUE:
                self.apply_border_style("#2E3192")

    def _setup_layouts(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.header_widget.separator)
        self.layout.addWidget(self.turns_widget)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(sizePolicy)

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(
            f"#AttrBox {{ "
            f"border: {self.attr_panel.filter_tab.attr_box_border_width}px solid {color_hex};"
            f" border-style: inset; "
            f"}}"
        )

    ### CREATE LABELS ###

    def resize_attr_box(self) -> None:
        for button in self.rot_dir_button_manager.buttons:
            button.setMinimumSize(
                self.attr_panel.width() // 20, self.attr_panel.width() // 20
            )
            button.setMaximumSize(
                self.attr_panel.width() // 20, self.attr_panel.width() // 20
            )
            button.setIconSize(button.size())
        self.turns_widget.resize_turns_widget()
