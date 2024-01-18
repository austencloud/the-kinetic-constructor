from typing import TYPE_CHECKING
from constants import (
    MOTION_TYPE,
)
from utilities.TypeChecking.TypeChecking import MotionTypes
from objects.motion.motion import Motion
from widgets.attr_box.rot_dir_button_manager import RotDirButtonManager
from widgets.header_widget import HeaderWidget

from .attr_box_widgets.turns_widget.motion_type_turns_widget import (
    MotionTypeTurnsWidget,
)
from .base_attr_box import AttrBox


if TYPE_CHECKING:
    from widgets.attr_panel.base_attr_panel import BaseAttrPanel


class MotionTypeAttrBox(AttrBox):
    def __init__(self, attr_panel: "BaseAttrPanel", motion_type: MotionTypes) -> None:
        super().__init__(attr_panel, MOTION_TYPE)
        self.attribute_type = MOTION_TYPE
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        self.rot_dir_button_manager = RotDirButtonManager(self)
        self.header_widget = HeaderWidget(self)
        self.turns_widget = MotionTypeTurnsWidget(self)
        self.vbox_layout.addWidget(self.header_widget, 1)
        self.vbox_layout.addWidget(self.turns_widget, 2)
