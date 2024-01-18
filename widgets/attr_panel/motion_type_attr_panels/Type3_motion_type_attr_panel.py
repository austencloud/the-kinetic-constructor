from constants import ANTI, DASH, PRO, SHIFT, STATIC
from typing import TYPE_CHECKING, List


from ...attr_box.motion_type_attr_box import MotionTypeAttrBox
from ...attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class Type3MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, scroll_area: "ScrollArea") -> None:
        super().__init__(scroll_area)

        self.setup_layouts()
        self.shift_attr_box = MotionTypeAttrBox(self, SHIFT)
        self.dash_attr_box = MotionTypeAttrBox(self, DASH)

        self.pro_attr_box = MotionTypeAttrBox(self, PRO)
        self.anti_attr_box = MotionTypeAttrBox(self, ANTI)

        self.boxes: List[MotionTypeAttrBox] = [
            self.shift_attr_box,
            self.pro_attr_box,
            self.anti_attr_box,
            self.dash_attr_box,
        ]

        for box in self.boxes:
            self.layout.addWidget(box)
