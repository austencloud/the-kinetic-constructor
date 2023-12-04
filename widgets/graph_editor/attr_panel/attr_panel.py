from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from settings.string_constants import RED, BLUE
from utilities.TypeChecking.TypeChecking import Colors
from widgets.graph_editor.attr_panel.attr_box import AttrBox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class AttrPanel(QFrame):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()

        self.pictograph = pictograph

        self.setFixedHeight(self.pictograph.graph_editor.height())
        self.setFixedWidth(int(self.pictograph.graph_editor.width() * 0.4))

        self.setContentsMargins(0, 0, 0, 0)

        self.blue_attr_box = AttrBox(self, pictograph, BLUE)
        self.red_attr_box = AttrBox(self, pictograph, RED)
        self.attr_panel_layout = QHBoxLayout()
        self.setLayout(self.attr_panel_layout)
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.attr_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.attr_panel_layout.setSpacing(0)
        self.attr_panel_layout.addWidget(self.blue_attr_box)
        self.attr_panel_layout.addWidget(self.red_attr_box)

    def update_panel(self, motion_color: Colors) -> None:
        motion = self.pictograph.get_motion_by_color(motion_color)
        
        if motion_color == BLUE:
            self.blue_attr_box.update_attr_box(motion)
        elif motion_color == RED:
            self.red_attr_box.update_attr_box(motion)

    def update_attr_panel_size(self) -> None:
        self.setFixedHeight(self.pictograph.view.height())
        self.setFixedWidth(int(self.pictograph.graph_editor.width() * 0.6))

        self.blue_attr_box.update_attr_box_size()
        self.red_attr_box.update_attr_box_size()

    def clear_all_attr_boxes(self) -> None:
        self.blue_attr_box.clear_attr_box()
        self.red_attr_box.clear_attr_box()