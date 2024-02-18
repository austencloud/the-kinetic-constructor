from constants import BLUE, RED
from typing import TYPE_CHECKING
from objects.motion.motion import Motion
from PyQt6.QtWidgets import QFrame
from .GE_adjustment_box import GE_AdjustmentBox

if TYPE_CHECKING:
    from .graph_editor import GraphEditor


class GE_AdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        super().__init__(graph_editor)
        self.setup_layouts()

    def _setup_attr_boxes(self) -> None:
        self.blue_attr_box: GE_AdjustmentBox = GE_AdjustmentBox(
            self, self.graph_editor.GE_pictograph, BLUE
        )
        self.red_attr_box: GE_AdjustmentBox = GE_AdjustmentBox(
            self, self.graph_editor.GE_pictograph, RED
        )
        self.boxes = [self.blue_attr_box, self.red_attr_box]

    def setup_layouts(self) -> None:
        self._setup_attr_boxes()

    # def showEvent(self, event) -> None:
    #     super().showEvent(event)
    #     max_width = int((self.graph_editor.main_widget.width()))
    #     self.setMaximumWidth(
    #         int(min(self.graph_editor.main_widget.width() / 3, max_width))
    #     )
    #     for box in [self.blue_attr_box, self.red_attr_box]:
    #         box.resize_graph_editor_attr_box()

    #     self.turns_panel_content_width = int(
    #         self.blue_attr_box.width() + self.red_attr_box.width()
    #     )

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
