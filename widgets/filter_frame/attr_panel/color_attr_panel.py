from constants import (
    BLUE,
    RED,
)
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import Colors, Turns
from widgets.filter_frame.attr_box.color_attr_box import ColorAttrBox
from widgets.filter_frame.attr_panel.base_attr_panel import BaseAttrPanel


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

    def get_turns_for_color(self, color: Colors) -> Turns:
        for box in self.boxes:
            if box.color == color:
                if box.turns_widget.turn_display_manager.turns_display.text() in [
                    "0",
                    "1",
                    "2",
                    "3",
                ]:
                    return int(
                        box.turns_widget.turn_display_manager.turns_display.text()
                    )
                elif box.turns_widget.turn_display_manager.turns_display.text() in [
                    "0.5",
                    "1.5",
                    "2.5",
                ]:
                    return float(
                        box.turns_widget.turn_display_manager.turns_display.text()
                    )
