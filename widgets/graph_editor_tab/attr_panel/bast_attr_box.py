from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from Enums import Color
from constants import HEX_BLUE, HEX_RED, RED
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
    from widgets.image_generator_tab.ig_attr_box import (
        IGAttrBox,
    )
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.base_attr_panel import (
        BaseAttrPanel,
    )


class BaseAttrBox(QFrame):
    def __init__(
        self, attr_panel: "BaseAttrPanel", pictograph: "Pictograph", color: Color
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[BaseAttrBoxWidget] = []
        self.combobox_border = 2
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
        self.apply_border_style(HEX_RED if self.color == RED else HEX_BLUE)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 3
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; border-style: inset; }}"
        )

    ### CREATE LABELS ###

    def clear_attr_box(self: Union["IGAttrBox", "GraphEditorAttrBox"]) -> None:
        self.start_end_loc_widget.clear_start_end_boxes()
        self.turns_widget.turnbox.setCurrentIndex(-1)
        self.turns_widget._update_clocks(None)
