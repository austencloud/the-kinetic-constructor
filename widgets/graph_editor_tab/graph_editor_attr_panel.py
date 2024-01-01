from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from constants import BLUE, RED
from objects.motion.motion import Motion
from typing import TYPE_CHECKING, Literal, Union
from widgets.image_generator_tab.ig_attr_box import IGAttrBox

from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import GraphEditorAttrBox

from widgets.graph_editor_tab.attr_panel.base_attr_panel import BaseAttrPanel

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.graph_editor_tab.graph_editor import GraphEditor
from PyQt6.QtCore import Qt


class GraphEditorAttrPanel(BaseAttrPanel):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.blue_attr_box: GraphEditorAttrBox = GraphEditorAttrBox(
            self, self.graph_editor.main_pictograph, BLUE
        )
        self.red_attr_box: GraphEditorAttrBox = GraphEditorAttrBox(
            self, self.graph_editor.main_pictograph, RED
        )
        self.setup_layouts()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        max_width = int(
            (
                self.graph_editor.main_widget.width()
                - self.graph_editor.main_widget.sequence_widget.width()
            )
        )
        self.setMaximumWidth(
            int(min(self.graph_editor.main_widget.width() / 3, max_width))
        )
        for box in [self.blue_attr_box, self.red_attr_box]:
            box.resize_graph_editor_attr_box()

        self.attr_panel_content_width = int(
            self.blue_attr_box.width()
            + self.red_attr_box.width()
            + self.red_attr_box.border_width / 2
        )
