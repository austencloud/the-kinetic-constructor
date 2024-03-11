from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from constants import BLUE, RED
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

    def set_turns(self, blue_turns: int, red_turns: int) -> None:
        self.blue_turns_box.turns_widget.display_manager.update_turns_display(
            blue_turns
        )
        self.red_turns_box.turns_widget.display_manager.update_turns_display(red_turns)

    def _setup_placeholder_widget(self) -> None:
        self.placeholder_widget = GE_PlaceHolderTextLabel(self)

    def _setup_turns_boxes(self) -> None:
        self.blue_turns_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, BLUE
        )
        self.red_turns_box: GE_TurnsBox = GE_TurnsBox(
            self, self.graph_editor.GE_pictograph, RED
        )
        self.turns_boxes = [self.blue_turns_box, self.red_turns_box]

    def _setup_start_pos_ori_pickers(self) -> None:
        self.blue_start_pos_ori_picker = GE_StartPosOriPickerBox(
            self, self.graph_editor.GE_pictograph, BLUE
        )
        self.red_start_pos_ori_picker = GE_StartPosOriPickerBox(
            self, self.graph_editor.GE_pictograph, RED
        )
        self.start_pos_ori_pickers = [
            self.blue_start_pos_ori_picker,
            self.red_start_pos_ori_picker,
        ]

    def update_adjustment_panel(self) -> None:
        pictograph = self.graph_editor.GE_pictograph_view.get_current_pictograph()
        if pictograph.is_blank:
            self.show_placeholder_widget()
            self.hide_start_pos_ori_pickers()
            self.hide_turns_boxes()
            QApplication.processEvents()
        elif self.graph_editor.GE_pictograph_view.is_start_pos:
            self.hide_placeholder_widget()
            self.hide_turns_boxes()
            self.show_start_pos_ori_pickers()
            QApplication.processEvents()
        else:
            self.hide_placeholder_widget()
            self.hide_start_pos_ori_pickers()
            self.show_turns_boxes()
            QApplication.processEvents()

    def hide_start_pos_ori_pickers(self) -> None:
        for picker in self.start_pos_ori_pickers:
            if picker.isVisible():
                picker.hide()

    def hide_turns_boxes(self) -> None:
        for turns_box in self.turns_boxes:
            if turns_box.isVisible():
                turns_box.hide()

    def show_placeholder_widget(self) -> None:
        if not self.placeholder_widget.isVisible():
            self.placeholder_widget.show()

    def hide_placeholder_widget(self) -> None:
        self.placeholder_widget.hide()

    def show_start_pos_ori_pickers(self) -> None:
        for picker in self.start_pos_ori_pickers:
            if not picker.isVisible():
                picker.show()

    def show_turns_boxes(self) -> None:
        for turns_box in self.turns_boxes:
            if not turns_box.isVisible():

                turns_box.show()

    def update_turns_panel(self, blue_turns: int, red_turns: int) -> None:
        self.set_turns(blue_turns, red_turns)
        for box in self.turns_boxes:
            box.header.update_turns_box_header()

    def resize_GE_adjustment_panel(self) -> None:
        self.setMinimumWidth(self.blue_turns_box.width() + self.red_turns_box.width())
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.update_adjustment_panel()
        for box in self.turns_boxes:
            box.resize_GE_turns_box()
        for ori_picker_box in self.start_pos_ori_pickers:
            ori_picker_box.resize_GE_ori_picker_box()
        self.placeholder_widget.set_stylesheet()
