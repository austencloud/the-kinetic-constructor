from Enums.MotionAttributes import Color
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout

from widgets.graph_editor.components.GE_start_pos_ori_picker import (
    GE_StartPosOriPickerBox,
)
from .GE_turns_box import GE_TurnsBox

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GE_AdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        super().__init__(graph_editor)
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self._setup_turns_boxes()
        self._setup_start_pos_ori_pickers()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        for box in self.boxes:
            self.layout.addWidget(box)

    def set_turns(self, blue_turns: int, red_turns: int) -> None:
        self.blue_adjustment_box.turns_widget.display_manager.update_turns_display(
            blue_turns
        )
        self.red_adjustment_box.turns_widget.display_manager.update_turns_display(
            red_turns
        )

    def _setup_turns_boxes(self) -> None:
        self.blue_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.BLUE
        )
        self.red_adjustment_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.RED
        )
        self.boxes = [self.blue_adjustment_box, self.red_adjustment_box]

    def _setup_start_pos_ori_pickers(self) -> None:
        self.blue_start_pos_ori_picker = GE_StartPosOriPickerBox(
            self, self.graph_editor.GE_pictograph, Color.BLUE
        )
        self.red_start_pos_ori_picker = GE_StartPosOriPickerBox(
            self, self.graph_editor.GE_pictograph, Color.RED
        )
        self.start_pos_ori_pickers = [
            self.blue_start_pos_ori_picker,
            self.red_start_pos_ori_picker,
        ]

    def resize_GE_adjustment_panel(self):
        for box in self.boxes:
            box.resize_GE_turns_box()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def update_turns_panel(self, blue_turns: int, red_turns: int) -> None:
        self.set_turns(blue_turns, red_turns)
        for box in self.boxes:
            box.header_widget.update_turns_box_header()
