from typing import TYPE_CHECKING
from constants import HEX_BLUE, HEX_RED, RED
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import Colors
from ..attr_box.attr_box_widgets.motion_types_widget import MotionTypeWidget
from ..attr_box.attr_box_widgets.start_end_loc_widget import StartEndLocWidget
from ..attr_box.attr_box import AttrBox
from ..attr_panel import AttrPanel
from ..buttons.adjust_turns_button import AdjustTurnsButton

from ..graph_editor_tab.graph_editor_header_widget import GraphEditorHeaderWidget
from ..graph_editor_tab.graph_editor_turns_widget import GraphEditorTurnsWidget


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


from PyQt6.QtGui import QFont


class GraphEditorAttrBox(AttrBox):
    def __init__(
        self, attr_panel: "AttrPanel", pictograph: "Pictograph", color: Colors
    ) -> None:
        super().__init__(attr_panel, pictograph)
        self.color = color
        self.pictograph = pictograph
        self._setup_widgets()
        self.apply_border_style(HEX_RED if self.color == RED else HEX_BLUE)

    def _setup_widgets(self) -> None:
        self.motion_type_widget = MotionTypeWidget(self)
        self.header_widget = GraphEditorHeaderWidget(self)
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
        self.motion_type_widget.clear_motion_type_box()

    def resize_graph_editor_attr_box(self) -> None:
        self.setMinimumWidth(int(self.pictograph.view.width() * 0.85))
        self.setMaximumWidth(int(self.pictograph.view.width() * 0.85))
        self.setMinimumHeight(self.pictograph.view.height())
        self.setMaximumHeight(self.pictograph.view.height())

        for button in self.findChildren(AdjustTurnsButton):
            button.update_adjust_turns_button_size(int(self.width() / 8))

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

    def update_attr_box(self, motion: Motion) -> None:
        self.start_end_loc_widget.update_start_end_loc_boxes(
            motion.start_loc, motion.end_loc
        )
        self.motion_type_widget.update_motion_type_box(motion.motion_type)
