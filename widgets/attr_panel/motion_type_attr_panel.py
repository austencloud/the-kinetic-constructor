from constants import ANTI, DASH, MOTION_TYPE, PRO, SHIFT, STATIC
from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.attr_box.base_attr_box import AttrBox
from .base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(
        self, filter_tab: "FilterTab", motion_types: List[MotionTypes]
    ) -> None:
        super().__init__(filter_tab)
        self.setup_layouts()
        self._setup_boxes(motion_types)

    def _setup_boxes(self, motion_types: List[str]) -> None:
        self.boxes: List[AttrBox] = []

        for motion_type in motion_types:
            if motion_type == PRO:
                self.boxes.append(AttrBox(self, MOTION_TYPE, PRO))
            elif motion_type == ANTI:
                self.boxes.append(AttrBox(self, MOTION_TYPE, ANTI))
            elif motion_type == DASH:
                self.boxes.append(AttrBox(self, MOTION_TYPE, DASH))
            elif motion_type == STATIC:
                self.boxes.append(AttrBox(self, MOTION_TYPE, STATIC))

        for box in self.boxes:
            self.layout.addWidget(box)
