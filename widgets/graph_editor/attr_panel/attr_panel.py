from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from PyQt6.QtGui import QResizeEvent
from constants.string_constants import RED, BLUE
from utilities.TypeChecking.TypeChecking import Colors
from widgets.graph_editor.attr_panel.attr_box import AttrBox
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.graph_editor import GraphEditor


class AttrPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.graph_editor = graph_editor
        self.setContentsMargins(0, 0, 0, 0)

        self.blue_attr_box = AttrBox(self, self.graph_editor.pictograph, BLUE)
        self.red_attr_box = AttrBox(self, self.graph_editor.pictograph, RED)
        self.attr_panel_layout = QHBoxLayout()
        self.setLayout(self.attr_panel_layout)
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.attr_panel_layout.setContentsMargins(0, 0, 0, 0)
        self.attr_panel_layout.setSpacing(0)
        self.attr_panel_layout.addWidget(self.blue_attr_box)
        self.attr_panel_layout.addWidget(self.red_attr_box)

    def update_attr_panel(self, motion_color: Colors) -> None:
        motion = self.graph_editor.pictograph.get_motion_by_color(motion_color)
        if motion_color == BLUE:
            self.blue_attr_box.update_attr_box(motion)
        elif motion_color == RED:
            self.red_attr_box.update_attr_box(motion)

    def clear_all_attr_boxes(self) -> None:
        self.blue_attr_box.clear_attr_box()
        self.red_attr_box.clear_attr_box()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.setMaximumWidth(self.blue_attr_box.width() + self.red_attr_box.width())
