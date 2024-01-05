from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from typing import TYPE_CHECKING, Union

from widgets.attr_panel.bast_attr_box import BaseAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


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

    def clear_all_attr_boxes(self) -> None:
        for box in self.boxes:
            box.clear_attr_box()
