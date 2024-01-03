from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from constants import BLUE, RED
from objects.motion.motion import Motion
from typing import TYPE_CHECKING, Union

from widgets.attr_panel.bast_attr_box import BaseAttrBox


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_panel import GraphEditorAttrPanel
    from widgets.ig_tab.ig_attr_panel import IGAttrPanel
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame
from PyQt6.QtCore import Qt


class BaseAttrPanel(QFrame):
    def __init__(
        self,
        parent: Union["GraphEditorFrame", "IGTab"],
    ) -> None:
        super().__init__()
        self.parent: Union["GraphEditorFrame", "IGTab"] = parent
        self.setContentsMargins(0, 0, 0, 0)
        self.blue_attr_box: BaseAttrBox = None
        self.red_attr_box: BaseAttrBox = None

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.blue_attr_box)
        self.layout.addWidget(self.red_attr_box)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def update_attr_panel(
        self: Union["GraphEditorAttrPanel", "IGAttrPanel"], motion: Motion
    ) -> None:
        if motion.motion_type:
            if motion.color == BLUE:
                self.blue_attr_box.update_attr_box(motion)
            elif motion.color == RED:
                self.red_attr_box.update_attr_box(motion)
        else:
            if motion.color == BLUE:
                self.blue_attr_box.clear_attr_box()
            elif motion.color == RED:
                self.red_attr_box.clear_attr_box()

    def clear_all_attr_boxes(self) -> None:
        self.blue_attr_box.clear_attr_box()
        self.red_attr_box.clear_attr_box()
