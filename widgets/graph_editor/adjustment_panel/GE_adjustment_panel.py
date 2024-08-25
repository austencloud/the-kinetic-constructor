from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from data.constants import BLUE, RED
from widgets.graph_editor.adjustment_panel.GE_placeholder_text_label import (
    GE_PlaceHolderTextLabel,
)

from widgets.graph_editor.adjustment_panel.turns_box.GE_turns_box import GE_TurnsBox
from widgets.graph_editor.ori_picker_box.GE_ori_picker_box import (
    GE_OriPickerBox,
)


if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor


class GE_AdjustmentPanel(QFrame):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        self.GE_pictograph = graph_editor.pictograph_container.GE_pictograph
        self.initialized = False
        super().__init__(graph_editor)
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self._setup_turns_boxes()
        self._setup_start_pos_ori_pickers()
        self._setup_placeholder_widget()
        self.layout: QHBoxLayout = QHBoxLayout(self)
        for box in self.turns_boxes:
            self.layout.addWidget(box)
        for ori_picker in self.ori_picker_boxes:
            self.layout.addWidget(ori_picker)
        self.layout.addWidget(self.placeholder_widget)

    def update_turns_displays(self, blue_turns: int, red_turns: int) -> None:
        self.blue_turns_box.turns_widget.update_turns_display(blue_turns)

        self.red_turns_box.turns_widget.update_turns_display(red_turns)

    def _setup_placeholder_widget(self) -> None:
        self.placeholder_widget = GE_PlaceHolderTextLabel(self)

    def _setup_turns_boxes(self) -> None:
        self.blue_turns_box: GE_TurnsBox = GE_TurnsBox(self, self.GE_pictograph, BLUE)
        self.red_turns_box: GE_TurnsBox = GE_TurnsBox(self, self.GE_pictograph, RED)
        self.turns_boxes = [self.blue_turns_box, self.red_turns_box]

    def _setup_start_pos_ori_pickers(self) -> None:
        self.blue_ori_picker = GE_OriPickerBox(self, self.GE_pictograph, BLUE)
        self.red_ori_picker = GE_OriPickerBox(self, self.GE_pictograph, RED)
        self.ori_picker_boxes = [self.blue_ori_picker, self.red_ori_picker]

    def update_adjustment_panel(self) -> None:
        pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        if pictograph.is_blank:
            self.show_placeholder_widget()
            self.hide_start_pos_ori_pickers()
            self.hide_turns_boxes()

        elif self.graph_editor.pictograph_container.GE_pictograph_view.is_start_pos:
            self.hide_placeholder_widget()
            self.hide_turns_boxes()
            self.show_start_pos_ori_pickers()

        else:
            self.hide_placeholder_widget()
            self.hide_start_pos_ori_pickers()
            self.show_turns_boxes()

        self.resize_GE_adjustment_panel()

    def hide_start_pos_ori_pickers(self) -> None:
        for picker in self.ori_picker_boxes:
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
        for picker in self.ori_picker_boxes:
            if not picker.isVisible():
                picker.show()
                picker.update_styled_border()

    def show_turns_boxes(self) -> None:
        for turns_box in self.turns_boxes:
            if not turns_box.isVisible():
                turns_box.show()
                turns_box.update_styled_border()

    def update_turns_panel(self, blue_turns: int, red_turns: int) -> None:
        self.update_turns_displays(blue_turns, red_turns)
        for box in self.turns_boxes:
            box.header.update_turns_box_header()

    def resize_GE_adjustment_panel(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        for turns_box in self.turns_boxes:
            turns_box.resize_turns_box()

        for ori_picker_box in self.ori_picker_boxes:
            ori_picker_box.resize_ori_picker_box()

        self.placeholder_widget.set_stylesheet()
