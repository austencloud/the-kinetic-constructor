from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from Enums import Color
from constants import HEX_BLUE, HEX_RED, RED
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
    from widgets.image_generator_tab.ig_filter_frame_attr_box import (
        IGFilterFrameAttrBox,
    )
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.attr_panel import (
        AttrPanel,
    )


class BaseAttrBox(QFrame):
    def __init__(
        self, attr_panel: "AttrPanel", pictograph: "Pictograph", color: Color
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self) -> None:
        self.setup_box()
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")
        self.apply_border_style(HEX_RED if self.color == RED else HEX_BLUE)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 3
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; border-style: inset; }}"
        )

    ### CREATE LABELS ###

    def clear_attr_box(
        self: Union["IGFilterFrameAttrBox", "GraphEditorAttrBox"]
    ) -> None:
        self.start_end_widget.clear_start_end_boxes()
        self.turns_widget.turnbox.setCurrentIndex(-1)
        self.turns_widget.update_clocks(None)

    def update_attr_box(
        self: Union["IGFilterFrameAttrBox", "GraphEditorAttrBox"], motion: Motion = None
    ) -> None:
        self.turns_widget.update_clocks(motion.prop_rot_dir)
        self.start_end_widget.update_start_end_boxes(motion.start_loc, motion.end_loc)
        if motion.prop_rot_dir:
            self.turns_widget.update_turnbox(motion.turns)

    def resize_attr_box(
        self: Union["IGFilterFrameAttrBox", "GraphEditorAttrBox"]
    ) -> None:
        if self.pictograph:  # for within the graph editor
            self.setMinimumWidth(int(self.pictograph.view.width() * 0.85))
            self.setMaximumWidth(int(self.pictograph.view.width() * 0.85))
            self.setMinimumHeight(self.pictograph.view.height())
            self.setMaximumHeight(self.pictograph.view.height())
        else:
            self.setMinimumWidth(int(self.attr_panel.width() / 2))
            self.setMaximumWidth(int(self.attr_panel.width() / 2))
            self.setMinimumHeight(int(self.attr_panel.height() / 5))
            self.setMaximumHeight(int(self.attr_panel.height() / 5))

        for button in self.findChildren(CustomButton):
            button.update_custom_button_size(int(self.width() / 8))

        self.header_spacing = int(self.width() * 0.02)
        ratio_total = 1 + 1 + 1 + 2
        available_height = self.height()
        header_height = int(available_height * (1 / ratio_total))
        start_end_height = int(available_height * (1 / ratio_total))
        turns_widget_height = int(available_height * (2 / ratio_total))
        self.header_widget.setMaximumHeight(header_height)
        self.start_end_widget.setMaximumHeight(start_end_height)
        self.turns_widget.setMaximumHeight(turns_widget_height)

        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.start_end_widget.resize_start_end_widget()

        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))
