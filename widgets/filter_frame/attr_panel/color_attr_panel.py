from constants import BLUE, RED
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import Colors, Turns
from widgets.filter_frame.attr_box.color_attr_box import ColorAttrBox
from widgets.filter_frame.attr_panel.base_attr_panel import BaseAttrPanel


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab


class ColorAttrPanel(BaseAttrPanel):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.blue_attr_box = ColorAttrBox(
            self, self.ig_tab.scroll_area.pictographs, BLUE
        )
        self.red_attr_box = ColorAttrBox(self, self.ig_tab.scroll_area.pictographs, RED)
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

    def resize_ig_color_attr_panel(self) -> None:
        self.layout.setSpacing(int(self.blue_attr_box.width() / 5))
        for box in self.boxes:
            box.resize_ig_color_attr_box()

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turn_display_manager.turns_display.setText("0")
            # if the box has buttons, set them to deselected
            if box.same_button:
                box.same_button.setStyleSheet(
                    box.turns_widget.get_vtg_dir_btn_style(pressed=False)
                )
                box.opp_button.setStyleSheet(
                    box.turns_widget.get_vtg_dir_btn_style(pressed=False)
                )
