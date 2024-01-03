from constants import ANTI, BLUE, DASH, PRO, RED, STATIC
from typing import TYPE_CHECKING, List
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.ig_tab.ig_attr_box import IGAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.pro_attr_box = IGAttrBox(self, self.ig_tab.ig_scroll_area.pictographs, PRO)
        self.anti_attr_box = IGAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, ANTI
        )
        self.dash_attr_box = IGAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, DASH
        )
        self.static_attr_box = IGAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, STATIC
        )
        self.boxes: List[IGAttrBox] = [
            self.pro_attr_box,
            self.anti_attr_box,
            self.dash_attr_box,
            self.static_attr_box,
        ]
        self.setup_layouts()

    def setup_layouts(self) -> None:
        super().setup_layouts()
        self.layout.addWidget(self.pro_attr_box)
        self.layout.addWidget(self.anti_attr_box)
        self.layout.addWidget(self.dash_attr_box)
        self.layout.addWidget(self.static_attr_box)

    def resize_ig_attr_panel(self) -> None:
        for box in self.boxes:
            box.resize_ig_attr_box()
        self.setMaximumWidth(self.pro_attr_box.width() * 4)
