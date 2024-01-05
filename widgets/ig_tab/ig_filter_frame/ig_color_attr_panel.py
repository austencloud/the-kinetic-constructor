from constants import ANTI, DASH, PRO, STATIC
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.ig_tab.ig_filter_frame.ig_motion_attr_box import IGMotionAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class IGColorAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.pro_attr_box = IGMotionAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, PRO
        )
        self.anti_attr_box = IGMotionAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, ANTI
        )
        self.dash_attr_box = IGMotionAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, DASH
        )
        self.static_attr_box = IGMotionAttrBox(
            self, self.ig_tab.ig_scroll_area.pictographs, STATIC
        )
        self.boxes: List[IGMotionAttrBox] = [
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
        self.layout.setSpacing(int(self.pro_attr_box.width() / 5))
        for box in self.boxes:
            box.resize_ig_attr_box()
        self.setMinimumWidth(self.pro_attr_box.width() * 4 + self.layout.spacing() * 3)
        self.setMaximumWidth(self.pro_attr_box.width() * 4 + self.layout.spacing() * 3)

    def get_turns_for_motion_type(self, motion_type: MotionTypes) -> int:
        for box in self.boxes:
            if box.motion_type == motion_type:
                if box.turns_widget.turnbox.currentText() in ["0", "1", "2", "3"]:
                    return int(box.turns_widget.turnbox.currentText())
                elif box.turns_widget.turnbox.currentText() in ["0.5", "1.5", "2.5"]:
                    return float(box.turns_widget.turnbox.currentText())
