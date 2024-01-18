from PyQt6.QtWidgets import QHBoxLayout, QFrame
from typing import TYPE_CHECKING, List

from constants import (
    BLUE,
    BLUE_PROP_ROT_DIR,
    BLUE_TURNS,
    DASH,
    NO_ROT,
    RED,
    RED_PROP_ROT_DIR,
    RED_TURNS,
    STATIC,
)
from ..attr_box.color_attr_box import ColorAttrBox
from ..attr_box.lead_state_attr_box import LeadStateAttrBox
from ..attr_box.motion_type_attr_box import MotionTypeAttrBox


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_tab import GraphEditorTab
    from widgets.ig_tab.ig_tab import IGTab


class BaseAttrPanel(QFrame):
    def __init__(self, parent_tab) -> None:
        super().__init__()
        self.boxes: List[MotionTypeAttrBox, ColorAttrBox, LeadStateAttrBox] = []
        self.parent_tab: "IGTab" | "GraphEditorTab" = parent_tab

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def clear_all_attr_boxes(self) -> None:
        for box in self.boxes:
            box.clear_attr_box()

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turns_display_manager.turns_display.setText("0")
            if hasattr(box, "header_widget"):
                for button in (
                    box.header_widget.vtg_dir_buttons
                    + box.header_widget.prop_rot_dir_buttons
                ):
                    button.unpress()
        for pictograph in self.parent_tab.scroll_area.pictographs.values():
            pictograph_dict = {
                BLUE_TURNS: 0,
                RED_TURNS: 0,
            }
            if pictograph.has_a_dash() or pictograph.has_a_static_motion():
                if pictograph.motions[BLUE].motion_type in [DASH, STATIC]:
                    pictograph_dict[BLUE_PROP_ROT_DIR] = NO_ROT
                elif pictograph.motions[RED].motion_type in [DASH, STATIC]:
                    pictograph_dict[RED_PROP_ROT_DIR] = NO_ROT

            pictograph.state_updater.update_pictograph(pictograph_dict)

    def resize_attr_panel(self) -> None:
        for box in self.boxes:
            box.resize_attr_box()
