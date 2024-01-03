from constants import BLUE, RED
from typing import TYPE_CHECKING
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.ig_tab.ig_attr_box import IGAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.blue_attr_box: IGAttrBox = IGAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, BLUE
        )
        self.red_attr_box: IGAttrBox = IGAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, RED
        )
        self.setup_layouts()

    def resize_ig_attr_panel(self) -> None:
        self.setMaximumWidth(
            int(self.ig_tab.width() - self.ig_tab.button_panel.width())
        )
        for box in [self.blue_attr_box, self.red_attr_box]:
            box.resize_ig_attr_box()
