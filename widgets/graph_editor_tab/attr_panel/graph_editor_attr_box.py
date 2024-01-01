from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from Enums import Color
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box import AttrBox
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.attr_panel import (
        AttrPanel,
    )
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.motion_types_widget import (
    MotionTypeWidget,
)


class GraphEditorAttrBox(AttrBox):
    def __init__(
        self, attr_panel: "AttrPanel", pictograph: "Pictograph", color: Color
    ) -> None:
        super().__init__(attr_panel, pictograph, color)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache

    def _setup_widgets(self) -> None:
        super()._setup_widgets() # set up base widgets plus motion type widget
        self.motion_type_widget = MotionTypeWidget(self) 
        self.layout.addWidget(self.motion_type_widget)

    ### CREATE LABELS ###

    def clear_attr_box(self) -> None:
        super ().clear_attr_box()
        self.motion_type_widget.clear_motion_type_box()


    def update_attr_box(self, motion: Motion = None) -> None:
        super().update_attr_box(motion)
        self.motion_type_widget.update_motion_type_box(motion.motion_type)

    def resize_attr_box(self) -> None:
        super().resize_attr_box()
        ratio_total = 1 + 1 + 1 + 2
        available_height = self.height()
        motion_types_height = int(available_height * (1 / ratio_total))
        self.motion_type_widget.setMaximumHeight(motion_types_height)
        self.motion_type_widget.resize_motion_type_widget()
