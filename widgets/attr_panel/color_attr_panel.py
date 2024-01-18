from constants import (
    BLUE,
    RED,
)
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import Colors, Turns
from widgets.attr_box.color_attr_box import ColorAttrBox
from widgets.attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class ColorAttrPanel(BaseAttrPanel):
    def __init__(self, parent_tab: "IGTab") -> None:
        super().__init__(parent_tab)
        self.scroll_area = parent_tab
        self.blue_attr_box = ColorAttrBox(self, BLUE)
        self.red_attr_box = ColorAttrBox(self, RED)
        self.boxes: List[ColorAttrBox] = [
            self.blue_attr_box,
            self.red_attr_box,
        ]

        self.setup_layouts()

    def setup_layouts(self) -> None:
        super().setup_layouts()
        for box in self.boxes:
            self.layout.addWidget(box)
        self.layout

