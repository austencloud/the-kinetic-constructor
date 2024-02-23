from Enums.MotionAttributes import Color
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from widgets.graph_editor.components.GE_placeholder_text import GE_PlaceHolderTextLabel
from widgets.graph_editor.components.GE_start_pos_ori_picker_box import (
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
        self._setup_placeholder_widget()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        for box in self.turns_boxes:
            self.layout.addWidget(box)
        for ori_picker in self.start_pos_ori_pickers:
            self.layout.addWidget(ori_picker)
        self.layout.addWidget(self.placeholder_widget)
        self.update_adjustment_panel()

    def set_turns(self, blue_turns: int, red_turns: int) -> None:
        self.blue_turns_box.turns_widget.display_manager.update_turns_display(
            blue_turns
        )
        self.red_turns_box.turns_widget.display_manager.update_turns_display(red_turns)

    def _setup_placeholder_widget(self) -> None:
        self.placeholder_widget = GE_PlaceHolderTextLabel(self)

    def _setup_turns_boxes(self) -> None:
        self.blue_turns_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.BLUE
        )
        self.red_turns_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, Color.RED
        )
        self.turns_boxes = [self.blue_turns_box, self.red_turns_box]

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
        for box in self.turns_boxes:
            box.resize_GE_turns_box()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.placeholder_widget.set_stylesheet()

    def update_adjustment_panel(self) -> None:
        if self.graph_editor.GE_pictograph_view.get_current_pictograph().is_blank:
            for picker in self.start_pos_ori_pickers:
                picker.hide()
            for turns_box in self.turns_boxes:
                turns_box.hide()
            self.placeholder_widget.show()
        elif self.graph_editor.GE_pictograph_view.is_start_pos:
            self.placeholder_widget.hide()
            for turns_box in self.turns_boxes:
                turns_box.hide()
            for picker in self.start_pos_ori_pickers:
                picker.show()
        else:
            self.placeholder_widget.hide()
            for picker in self.start_pos_ori_pickers:
                picker.hide()
            for turns_box in self.turns_boxes:
                turns_box.show()

    def update_turns_panel(self, blue_turns: int, red_turns: int) -> None:
        self.set_turns(blue_turns, red_turns)
        for box in self.turns_boxes:
            box.header_widget.update_turns_box_header()
        self.resize_GE_adjustment_panel()
