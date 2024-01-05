from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)


if TYPE_CHECKING:
    from widgets.attr_panel.base_attr_panel import BaseAttrPanel
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
    from widgets.ig_tab.ig_filter_frame.ig_motion_attr_box import (
        IGMotionAttrBox,
    )
    from objects.pictograph.pictograph import Pictograph


class BaseAttrBox(QFrame):
    def __init__(self, attr_panel: "BaseAttrPanel", pictograph: "Pictograph") -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.font_size = self.width() // 10
        self.widgets: List[BaseAttrBoxWidget] = []
        self.combobox_border = 2
        self.border_width = 3
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()

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

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; border-style: inset; }}"
        )

    ### CREATE LABELS ###

    def clear_attr_box(self: Union["IGMotionAttrBox", "GraphEditorAttrBox"]) -> None:
        self.start_end_loc_widget.clear_start_end_boxes()
        self.turns_widget.turnbox.setCurrentIndex(-1)
