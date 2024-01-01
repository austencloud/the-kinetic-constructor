from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtGui import QPixmap
from Enums import Color
from objects.motion.motion import Motion
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.graph_editor_turns_widget import GraphEditorTurnsWidget
from widgets.graph_editor_tab.attr_panel.bast_attr_box import BaseAttrBox
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.header_widget import (
    HeaderWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.start_end_loc_widget import (
    StartEndLocWidget,
)
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)
from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.attr_panel.base_attr_panel import (
        BaseAttrPanel,
    )
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.motion_types_widget import (
    MotionTypeWidget,
)
from PyQt6.QtGui import QPixmap, QFont


class GraphEditorAttrBox(BaseAttrBox):
    def __init__(
        self, attr_panel: "BaseAttrPanel", pictograph: "Pictograph", color: Color
    ) -> None:
        super().__init__(attr_panel, pictograph, color)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        self.motion_type_widget = MotionTypeWidget(self)
        self.header_widget = HeaderWidget(self)
        self.start_end_loc_widget = StartEndLocWidget(self)
        self.turns_widget = GraphEditorTurnsWidget(self)

        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.motion_type_widget)
        self.layout.addWidget(self.start_end_loc_widget)
        self.layout.addWidget(self.turns_widget)

    ### CREATE LABELS ###

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def clear_attr_box(self) -> None:
        super().clear_attr_box()
        self.motion_type_widget.clear_motion_type_box()

    def update_attr_box(self, motion: Motion = None) -> None:
        super().update_attr_box(motion)
        self.motion_type_widget.update_motion_type_box(motion.motion_type)

    def resize_graph_editor_attr_box(self) -> None:
        self.setMinimumWidth(int(self.pictograph.view.width() * 0.85))
        self.setMaximumWidth(int(self.pictograph.view.width() * 0.85))
        self.setMinimumHeight(self.pictograph.view.height())
        self.setMaximumHeight(self.pictograph.view.height())

        for button in self.findChildren(CustomButton):
            button.update_custom_button_size(int(self.width() / 8))

        self.header_spacing = int(self.width() * 0.02)
        ratio_total = 1 + 1 + 1 + 2
        available_height = self.height()
        header_height = int(available_height * (1 / ratio_total))
        start_end_height = int(available_height * (1 / ratio_total))
        turns_widget_height = int(available_height * (2 / ratio_total))
        self.header_widget.setMaximumHeight(header_height)
        self.start_end_loc_widget.setMaximumHeight(start_end_height)
        self.turns_widget.setMaximumHeight(turns_widget_height)

        self.header_widget.resize_header_widget()
        self.motion_type_widget.resize_motion_type_widget()
        self.turns_widget.resize_turns_widget()
        self.start_end_loc_widget.resize_start_end_widget()

        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))
