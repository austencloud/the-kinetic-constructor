from constants import BLUE, RED
from typing import TYPE_CHECKING
from objects.motion.motion import Motion
from PyQt6.QtWidgets import QFrame, QVBoxLayout
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
        self.layout:QVBoxLayout = QVBoxLayout(self)
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

    def resize_GE_adjustment_panel(self):
        self.setMaximumHeight(self.graph_editor.height())
        self.setMaximumWidth(self.graph_editor.width())
        for box in self.boxes:
            box.resize_GE_turns_box()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)