from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy

from constants import OPP, SAME
from utilities.TypeChecking.TypeChecking import MotionTypes
from .attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
    TurnsWidget,
)
from ..attr_box.attr_box_widgets.base_attr_box_widget import AttrBoxWidget

if TYPE_CHECKING:
    from ..graph_editor_tab.graph_editor_attr_box import GraphEditorAttrBox
    from ..attr_box.motion_type_attr_box import MotionTypeAttrBox
    from ..attr_panel.base_attr_panel import BaseAttrPanel
    from objects.pictograph.pictograph import Pictograph


class BaseAttrBox(QFrame):
    def __init__(self, attr_panel: "BaseAttrPanel", pictograph: "Pictograph") -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.turns_widget: TurnsWidget = None
        self.motion_type: MotionTypes = None
        self.combobox_border = 2
        self.border_width = 3
        self.pixmap_cache: Dict[str, QPixmap] = {}
        self.vtg_dir_btn_state: Dict[str, bool] = {SAME: True, OPP: False}
        self.init_ui()

    def init_ui(self) -> None:
        self.setup_box()
        self.vbox_layout: QVBoxLayout = QVBoxLayout()
        self.vbox_layout.setContentsMargins(0, 0, 0, 0)
        self.vbox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vbox_layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(
            f"#AttributeBox {{ "
            f"border: {self.border_width}px solid {color_hex};"
            f" border-style: inset; "
            f"}}"
        )

    ### CREATE LABELS ###

    def clear_attr_box(self: Union["MotionTypeAttrBox", "GraphEditorAttrBox"]) -> None:
        self.start_end_loc_widget.clear_start_end_boxes()

    def resize_attr_box(self) -> None:
        self.turns_widget.resize_turns_widget()
