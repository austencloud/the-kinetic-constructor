from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
)
from constants import BLUE, RED
from objects.motion.motion import Motion
from typing import TYPE_CHECKING, Union
from widgets.ig_tab.ig_filter_frame.ig_motion_attr_box import IGMotionAttrBox


if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame
from PyQt6.QtCore import Qt


class IGFilterFrame(QFrame):
    def __init__(
        self,
        parent: Union["GraphEditorFrame", "IGTab"],
    ) -> None:
        super().__init__()
        self.parent: Union["GraphEditorFrame", "IGTab"] = parent
        self.setContentsMargins(0, 0, 0, 0)

        self.blue_attr_box = IGMotionAttrBox(
            self, self.parent.ig_scroll_area.pictographs, BLUE
        )
        self.red_attr_box = IGMotionAttrBox(self, self.parent.ig_scroll_area, RED)
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

    # def resize_ig_filter_frame(self, event) -> None:
    #     super().showEvent(event)
    #     max_width = int((self.parent.width() - self.parent.button_panel.width())
    #     )
    # self.setMaximumWidth(int(min(self.parent.main_widget.width() / 3, max_width)))
    # for box in [self.blue_attr_box, self.red_attr_box]:
    #     box.resize_attr_box()

    # self.attr_panel_content_width = int(
    #     self.blue_attr_box.width()
    #     + self.red_attr_box.width()
    #     + self.red_attr_box.border_width / 2
    # )

    # self.setMaximumWidth(self.attr_panel_content_width)
    # self.setMinimumWidth(self.attr_panel_content_width)
