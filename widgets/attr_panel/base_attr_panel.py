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
        self.boxes: list[BaseAttrBox] = []
        
    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def clear_all_attr_boxes(self) -> None:
        for box in self.boxes:
            box.clear_attr_box()
