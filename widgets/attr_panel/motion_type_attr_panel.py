from constants import ANTI, DASH, PRO, SHIFT, STATIC
from typing import TYPE_CHECKING, List

from ..attr_box.motion_type_attr_box import MotionTypeAttrBox
from .base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, scroll_area: "ScrollArea", motion_types: List[str]) -> None:
        super().__init__(scroll_area)
        self.setup_layouts()
        self._setup_boxes(motion_types)

    def _setup_boxes(self, motion_types: List[str]) -> None:
        self.boxes: List[MotionTypeAttrBox] = []

        for motion_type in motion_types:
            if motion_type == SHIFT:
                self.boxes.append(MotionTypeAttrBox(self, SHIFT))
            elif motion_type == STATIC:
                self.boxes.append(MotionTypeAttrBox(self, STATIC))
            elif motion_type == DASH:
                self.boxes.append(MotionTypeAttrBox(self, DASH))
            elif motion_type == PRO:
                self.boxes.append(MotionTypeAttrBox(self, PRO))
            elif motion_type == ANTI:
                self.boxes.append(MotionTypeAttrBox(self, ANTI))

        for box in self.boxes:
            self.layout.addWidget(box)
