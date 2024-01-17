from constants import ANTI, PRO
from typing import TYPE_CHECKING, List


from ...attr_box.motion_type_attr_box import MotionTypeAttrBox
from ..base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class Type1MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, scroll_area: "ScrollArea") -> None:
        super().__init__(scroll_area)

        self.setup_layouts()

        self.pro_attr_box = MotionTypeAttrBox(self, PRO)
        self.anti_attr_box = MotionTypeAttrBox(self, ANTI)

        self.boxes: List[MotionTypeAttrBox] = [
            self.pro_attr_box,
            self.anti_attr_box,
        ]
        for box in self.boxes:
            self.layout.addWidget(box)
