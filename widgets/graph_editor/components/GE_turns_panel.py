from constants import BLUE, RED
from typing import TYPE_CHECKING
from objects.motion.motion import Motion
from PyQt6.QtWidgets import QFrame
from .GE_turns_box import GE_TurnsBox

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GE_AdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        super().__init__(graph_editor)
        self.setup_layouts()

    def _setup_attr_boxes(self) -> None:
        self.blue_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, BLUE
        )
        self.red_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, RED
        )
        self.boxes = [self.blue_adjustment_box, self.red_adjustment_box]

    def setup_layouts(self) -> None:
        self._setup_attr_boxes()

    def update_turns_panel(self, motion: Motion) -> None:
        if motion.motion_type:
            if motion.color == BLUE:
                self.blue_adjustment_box.update_attr_box(motion)
            elif motion.color == RED:
                self.red_adjustment_box.update_attr_box(motion)
        else:
            if motion.color == BLUE:
                self.blue_adjustment_box.clear_attr_box()
            elif motion.color == RED:
                self.red_adjustment_box.clear_attr_box()
