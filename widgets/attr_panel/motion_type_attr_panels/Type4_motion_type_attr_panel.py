from constants import ANTI, DASH, PRO, SHIFT, STATIC
from typing import TYPE_CHECKING, List


from ...attr_box.motion_type_attr_box import MotionTypeAttrBox
from ...attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class Type4MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, scroll_area: "ScrollArea") -> None:
        super().__init__(scroll_area)

        self.setup_layouts()
        self.dash_attr_box = MotionTypeAttrBox(self, DASH)
        self.static_attr_box = MotionTypeAttrBox(self, STATIC)

        self.boxes: List[MotionTypeAttrBox] = [
            self.dash_attr_box,
            self.static_attr_box,
        ]

        for box in self.boxes:
            self.layout.addWidget(box)
