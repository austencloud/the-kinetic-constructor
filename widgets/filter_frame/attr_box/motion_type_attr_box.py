from typing import TYPE_CHECKING, Dict, List
from constants import DASH, MOTION_TYPE, OPP, SAME, STATIC
from utilities.TypeChecking.TypeChecking import MotionTypes
from objects.motion.motion import Motion
from .attr_box_widgets.base_attr_box_widget import AttrBoxWidget
from .attr_box_widgets.turns_widgets.motion_type_turns_widget import (
    MotionTypeTurnsWidget,
)
from .base_attr_box import BaseAttrBox
from ...attr_box_widgets.header_widgets.motion_type_header_widget import (
    MotionTypeHeaderWidget,
)

if TYPE_CHECKING:
    from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QSizePolicy


class MotionTypeAttrBox(BaseAttrBox):
    def __init__(
        self,
        attr_panel: "MotionTypeAttrPanel",
        motion_type: MotionTypes,
    ) -> None:
        super().__init__(attr_panel, None)
        self.attr_panel = attr_panel
        self.motion_type = motion_type
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
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
            self.vtg_dir_btn_state = {SAME: False, OPP: False}

    def hide_buttons(self) -> None:
        for button in self.header_widget.prop_rot_dir_buttons:
            button.hide()

    def show_vtg_dir_buttons(self) -> None:
        for i in range(len(self.header_widget.prop_rot_dir_buttons)):
            self.header_widget.layout.replaceWidget(
                self.header_widget.prop_rot_dir_buttons[i],
                self.header_widget.vtg_dir_buttons[i],
            )
            self.header_widget.prop_rot_dir_buttons[i].hide()
            self.header_widget.vtg_dir_buttons[i].show()

    def show_prop_rot_dir_buttons(self) -> None:
        for i in range(len(self.header_widget.vtg_dir_buttons)):
            self.header_widget.layout.replaceWidget(
                self.header_widget.vtg_dir_buttons[i],
                self.header_widget.prop_rot_dir_buttons[i],
            )
            self.header_widget.vtg_dir_buttons[i].hide()
            self.header_widget.prop_rot_dir_buttons[i].show()

    def _setup_widgets(self) -> None:
        self.header_widget = MotionTypeHeaderWidget(self, self.motion_type)
        self.turns_widget = MotionTypeTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)

    def resize_ig_motion_type_attr_box(self) -> None:
        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()

    def get_pictographs(self) -> List["Pictograph"]:
        return list(self.attr_panel.parent_tab.scroll_area.pictographs.values())

    def update_attr_box(self, motion: Motion) -> None:
        self.turns_widget.turn_display_manager.update_turns_display(motion.turns)

    def resize_attr_box(self) -> None:
        self.turns_widget.resize_turns_widget()