from constants import (
    BLUE,
    COLOR,
    RED,
)
from typing import TYPE_CHECKING, List
from widgets.attr_box.base_attr_box import AttrBox
from widgets.attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab
    from widgets.ig_tab.ig_tab import IGTab


class ColorAttrPanel(BaseAttrPanel):
    def __init__(self, filter_tab: "FilterTab") -> None:
        super().__init__(filter_tab)
        self._setup_boxes()
        self.setup_layouts()

    def _setup_boxes(self) -> None:
        self.blue_attr_box = AttrBox(self, COLOR, BLUE)
        self.red_attr_box = AttrBox(self, COLOR, RED)
        self.boxes: List[AttrBox] = [
            self.blue_attr_box,
            self.red_attr_box,
        ]

    def setup_layouts(self) -> None:
        super().setup_layouts()
        for box in self.boxes:
            self.layout.addWidget(box)
