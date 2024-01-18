from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.buttons.prop_rot_dir_button import PropRotDirButton
from widgets.buttons.vtg_dir_button import VtgDirButton
from widgets.attr_box.attr_box_widgets.header_widgets.base_header_widget import (
    HeaderWidget,
)

if TYPE_CHECKING:
    from widgets.attr_box.motion_type_attr_box import MotionTypeAttrBox
from constants import (
    ANTI,
    DASH,
    PRO,
    STATIC,
)


class MotionTypeHeaderWidget(HeaderWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: "MotionTypeAttrBox" = attr_box
        self.header_label = self._setup_header_label(self.attr_box.motion_type.capitalize())

        if self.attr_box.motion_type in [PRO, ANTI]:
            self._setup_layout()
        if self.attr_box.motion_type in [DASH, STATIC]:
            self._setup_layout_with_vtg_dir_buttons()
