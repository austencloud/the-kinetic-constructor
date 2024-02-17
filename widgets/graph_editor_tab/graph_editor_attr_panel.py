from constants import BLUE, RED
from typing import TYPE_CHECKING
from objects.motion.motion import Motion
from widgets.turns_panel import TurnsPanel
from PyQt6.QtWidgets import QFrame
from ..graph_editor_tab.graph_editor_attr_box import GraphEditorTurnsBox

if TYPE_CHECKING:
    from ..graph_editor_tab.graph_editor_frame import GraphEditorFrame


class GraphEditorAttrPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditorFrame") -> None:
        self.graph_editor = graph_editor
        super().__init__(graph_editor)
        self.setup_layouts()

    def _setup_attr_boxes(self) -> None:
        self.blue_attr_box: GraphEditorTurnsBox = GraphEditorTurnsBox(
            self, self.graph_editor.main_pictograph, BLUE
        )
        self.red_attr_box: GraphEditorTurnsBox = GraphEditorTurnsBox(
            self, self.graph_editor.main_pictograph, RED
        )
        self.boxes = [self.blue_attr_box, self.red_attr_box]

    def setup_layouts(self) -> None:
        self._setup_attr_boxes()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        max_width = int(
            (
                self.graph_editor.main_widget.width()
            )
        )
        self.setMaximumWidth(
            int(min(self.graph_editor.main_widget.width() / 3, max_width))
        )
        for box in [self.blue_attr_box, self.red_attr_box]:
            box.resize_graph_editor_attr_box()

        self.turns_panel_content_width = int(
            self.blue_attr_box.width()
            + self.red_attr_box.width()
        )

    def update_turns_panel(self, motion: Motion) -> None:
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
