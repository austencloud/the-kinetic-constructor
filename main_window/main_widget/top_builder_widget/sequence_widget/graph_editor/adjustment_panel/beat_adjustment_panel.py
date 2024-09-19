from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from data.constants import BLUE, RED
from .adjustment_panel_placeholder_text import AdjustmentPanelPlaceHolderText

from .ori_picker_box.ori_picker_box import OriPickerBox
from .turns_box.turns_box import TurnsBox


if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from ..graph_editor import GraphEditor


class BeatAdjustmentPanel(QFrame):
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
            self.layout.addWidget(box, 1)
        for ori_picker in self.ori_picker_boxes:
            self.layout.addWidget(ori_picker)
        self.layout.addWidget(self.placeholder_widget)

    def update_turns_displays(
        self, blue_motion: "Motion", red_motion: "Motion"
    ) -> None:
        self.blue_turns_box.turns_widget.update_turns_display(
            blue_motion, blue_motion.turns
        )
        self.red_turns_box.turns_widget.update_turns_display(
            red_motion, red_motion.turns
        )

    def _setup_placeholder_widget(self) -> None:
        self.placeholder_widget = AdjustmentPanelPlaceHolderText(self)

    def _setup_turns_boxes(self) -> None:
        self.blue_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, BLUE)
        self.red_turns_box: TurnsBox = TurnsBox(self, self.GE_pictograph, RED)
        self.turns_boxes = [self.blue_turns_box, self.red_turns_box]

    def _setup_start_pos_ori_pickers(self) -> None:
        self.blue_ori_picker = OriPickerBox(self, self.GE_pictograph, BLUE)
        self.red_ori_picker = OriPickerBox(self, self.GE_pictograph, RED)
        self.ori_picker_boxes = [self.blue_ori_picker, self.red_ori_picker]

    def update_adjustment_panel(self) -> None:
        pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        if pictograph.is_blank:
            self.placeholder_widget.show()
            self.hide_start_pos_ori_pickers()
            self.hide_turns_boxes()

        elif self.graph_editor.pictograph_container.GE_pictograph_view.is_start_pos:
            self.placeholder_widget.hide()
            self.hide_turns_boxes()
            self.show_start_pos_ori_pickers()

        else:
            self.placeholder_widget.hide()
            self.hide_start_pos_ori_pickers()
            self.show_turns_boxes()


    def hide_start_pos_ori_pickers(self) -> None:
        for picker in self.ori_picker_boxes:
            picker.hide()

    def hide_turns_boxes(self) -> None:
        for turns_box in self.turns_boxes:
            turns_box.hide()

    def show_start_pos_ori_pickers(self) -> None:
        for ori_picker_box in self.ori_picker_boxes:
            ori_picker_box.show()

    def show_turns_boxes(self) -> None:
        for turns_box in self.turns_boxes:
            turns_box.show()

    def update_turns_panel(self, blue_motion: "Motion", red_motion: "Motion") -> None:
        self.update_turns_displays(blue_motion, red_motion)
        for box in self.turns_boxes:
            box.header.update_turns_box_header()
            if box.color == BLUE:
                box.matching_motion = blue_motion
            else:
                box.matching_motion = red_motion

    def resize_beat_adjustment_panel(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        for turns_box in self.turns_boxes:
            turns_box.resize_turns_box()

        for ori_picker_box in self.ori_picker_boxes:
            ori_picker_box.resize_ori_picker_box()

        self.placeholder_widget.resize_adjustment_panel_placeholder_text()
        # QApplication.processEvents()
