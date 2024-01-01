from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from constants import BLUE, RED
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import GraphEditorAttrBox
from typing import TYPE_CHECKING, Literal, Union
from widgets.image_generator_tab.ig_filter_frame_attr_box import IGFilterFrameAttrBox


if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab
    from widgets.graph_editor_tab.graph_editor import GraphEditor
from PyQt6.QtCore import Qt


class AttrPanel(QFrame):
    def __init__(
        self,
        parent: Union["GraphEditor", "IGTab"],
        panel_id: Literal["ig_tab", "graph_editor"],
    ) -> None:
        super().__init__()
        self.parent: Union["GraphEditor", "IGTab"] = parent
        self.setContentsMargins(0, 0, 0, 0)
        self.panel_id = panel_id
        if panel_id == "graph_editor":
            self.blue_attr_box = GraphEditorAttrBox(
                self, self.parent.main_pictograph, BLUE
            )
            self.red_attr_box = GraphEditorAttrBox(
                self, self.parent.main_pictograph, RED
            )
        elif panel_id == "ig_tab":
            self.blue_attr_box = IGFilterFrameAttrBox(
                self, self.parent.ig_scroll_area.pictographs, BLUE
            )
            self.red_attr_box = IGFilterFrameAttrBox(
                self, self.parent.ig_scroll_area, RED
            )
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.blue_attr_box)
        self.layout.addWidget(self.red_attr_box)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def update_attr_panel(self, motion: Motion) -> None:
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

    def clear_all_attr_boxes(self) -> None:
        self.blue_attr_box.clear_attr_box()
        self.red_attr_box.clear_attr_box()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        width = int(
            (
                self.parent.main_widget.width()
                - self.parent.main_widget.sequence_widget.width()
            )
            if self.panel_id == "graph_editor"
            else (
                self.parent.main_widget.width()
                - self.parent.main_widget.sequence_widget.width()
            )
        )
        self.setMaximumWidth(
            int(
                self.parent.main_widget.width()
                - self.parent.main_widget.sequence_widget.width()
            )
        )
        for box in [self.blue_attr_box, self.red_attr_box]:
            box.resize_attr_box()
        self.attr_panel_content_width = int(
            self.blue_attr_box.width()
            + self.red_attr_box.width()
            + self.red_attr_box.border_width / 2
        )

        self.setMaximumWidth(self.attr_panel_content_width)
        self.setMinimumWidth(self.attr_panel_content_width)
