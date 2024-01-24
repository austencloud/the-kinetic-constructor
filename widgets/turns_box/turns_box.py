from typing import TYPE_CHECKING, Dict, Union
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    LEAD_STATE,
    MOTION_TYPE,
    OPP,
    RED,
    SAME,
)
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LeadStates,
    MotionAttributes,
    MotionTypes,
)

from widgets.header_widget import HeaderWidget
from widgets.turns_box.turns_box_widgets.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from .turns_box_widgets.turns_widget.turns_widget import (
    TurnsWidget,
)

if TYPE_CHECKING:
    from ..turns_panel import TurnsPanel


class TurnsBox(QFrame):
    turns_widget: TurnsWidget

    def __init__(
        self,
        turns_panel,
        attribute_type: MotionAttributes,
        attribute: Union[MotionAttributes, Colors, LeadStates],
    ) -> None:
        super().__init__(turns_panel)
        self.attribute_type: MotionAttributes = attribute_type
        self.attribute_value: Union[MotionAttributes, Colors, LeadStates] = attribute
        self.turns_panel: "TurnsPanel" = turns_panel
        self.font_size = self.turns_panel.width() // 20
        self.turn_display_border = 2
        self.vtg_dir_btn_state: Dict[str, bool] = {SAME: True, OPP: False}
        self.prop_rot_dir_btn_state: Dict[str, bool] = {
            CLOCKWISE: True,
            COUNTER_CLOCKWISE: False,
        }
        self._setup_attribute_type()
        self._setup_widgets()
        self._setup_layouts()

    def _setup_attribute_type(self) -> None:
        if self.attribute_type == MOTION_TYPE:
            self.motion_type: MotionTypes = self.attribute_value
            self.attribute_value = self.motion_type
        elif self.attribute_type == COLOR:
            self.color: Colors = self.attribute_value
            self.attribute_value = self.color
        elif self.attribute_type == LEAD_STATE:
            self.lead_state: LeadStates = self.attribute_value
            self.attribute_value = self.lead_state

    def _setup_widgets(self) -> None:
        self.prop_rot_dir_button_manager = PropRotDirButtonManager(self)
        self.header_widget = HeaderWidget(self)
        self.turns_widget = TurnsWidget(self)

        if self.attribute_type == COLOR:
            if self.color == RED:
                self.apply_border_style("#ED1C24")
            elif self.color == BLUE:
                self.apply_border_style("#2E3192")
        else:
            self.apply_border_style("#000000")  # Black border

    def _setup_layouts(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.header_widget.separator)
        self.layout.addWidget(self.turns_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def apply_border_style(self, color_hex: str) -> None:
        border_width = (
            1
            if color_hex == "#000000"
            else self.turns_panel.filter_tab.attr_box_border_width
        )
        self.setStyleSheet(
            f"#TurnsBox {{ "
            f"border: {border_width}px solid {color_hex};"
            f" border-style: inset; "
            f"}}"
        )

    def sizeHint(self) -> QSize:
        width, height = 0, 0
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item.widget():  # Check if the item is a widget
                widget_size_hint = item.widget().sizeHint()
                width += widget_size_hint.width()
                height = max(height, widget_size_hint.height())
        return QSize(width, height)

    ### CREATE LABELS ###

    def resize_turns_box(self) -> None:
        for (
            button
        ) in self.turns_panel.filter_tab.section.vtg_dir_button_manager.vtg_dir_buttons:
            button.setMinimumSize(
                self.turns_panel.filter_tab.section.width() // 26,
                self.turns_panel.filter_tab.section.width() // 26,
            )
            button.setMaximumSize(
                self.turns_panel.filter_tab.section.width() // 26,
                self.turns_panel.filter_tab.section.width() // 26,
            )
            button.setIconSize(button.size() * 0.8)
        self.turns_widget.resize_turns_widget()
