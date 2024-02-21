from Enums.MotionAttributes import Color
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .GE_turns_box import GE_TurnsBox

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GE_TurnsPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        super().__init__(graph_editor)
        self.setup_layouts()

    def set_turns(self, blue_turns: int, red_turns: int) -> None:
        self.blue_adjustment_box.turns_widget.display_manager.update_turns_display(
            blue_turns
        )
        self.red_adjustment_box.turns_widget.display_manager.update_turns_display(
            red_turns
        )

    def _setup_attr_boxes(self) -> None:
        self.blue_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.BLUE
        )
        self.red_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.RED
        )
        self.boxes = [self.blue_adjustment_box, self.red_adjustment_box]

    def setup_layouts(self) -> None:
        self._setup_attr_boxes()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        for box in self.boxes:
            self.layout.addWidget(box)

    def resize_GE_adjustment_panel(self):
        for box in self.boxes:
            box.resize_GE_turns_box()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
