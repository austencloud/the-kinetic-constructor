from constants import ANTI, DASH, PRO, STATIC
from typing import TYPE_CHECKING, List, Union


from ...attr_box.motion_type_attr_box import MotionTypeAttrBox
from ...attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from ....option_picker_tab.option_picker_tab import OptionPickerTab
    from ....ig_tab.ig_tab import IGTab


class Type4MotionTypeAttrPanel(BaseAttrPanel):
    def __init__(self, parent_tab: Union["IGTab", "OptionPickerTab"]) -> None:
        super().__init__(parent_tab)
        self.scroll_area = parent_tab

        self.setup_layouts()

        self.pro_attr_box = MotionTypeAttrBox(self, PRO)
        self.anti_attr_box = MotionTypeAttrBox(self, ANTI)
        self.dash_attr_box = MotionTypeAttrBox(self, DASH)
        self.static_attr_box = MotionTypeAttrBox(self, STATIC)
        self.boxes: List[MotionTypeAttrBox] = [
            self.pro_attr_box,
            self.anti_attr_box,
            self.dash_attr_box,
            self.static_attr_box,
        ]
        for box in self.boxes:
            self.layout.addWidget(box)

