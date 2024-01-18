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
    def __init__(self, attr_box, motion_type: MotionTypes) -> None:
        super().__init__(attr_box)
        self.attr_box: "MotionTypeAttrBox" = attr_box
        self.motion_type = motion_type
        self.header_label = self._setup_header_label(self.motion_type.capitalize())

        if self.motion_type in [PRO, ANTI]:
            self._setup_layout()
        if self.motion_type in [DASH, STATIC]:
            self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()
            self.prop_rot_dir_buttons: List[
                PropRotDirButton
            ] = self._setup_prop_rot_dir_buttons()
            self._setup_layout_with_vtg_dir_buttons()
