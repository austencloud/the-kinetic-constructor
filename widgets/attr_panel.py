from PyQt6.QtWidgets import QHBoxLayout, QFrame
from typing import TYPE_CHECKING, List

from constants import (
    ANTI,
    BLUE,
    BLUE_PROP_ROT_DIR,
    BLUE_TURNS,
    COLOR,
    DASH,
    LEAD_STATE,
    LEADING,
    MOTION_TYPE,
    NO_ROT,
    PRO,
    RED,
    RED_PROP_ROT_DIR,
    RED_TURNS,
    STATIC,
    TRAILING,
)

from widgets.attr_box.attr_box import AttrBox
from data.letter_engine_data import letter_type_motion_type_map

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab

ATTRIBUTES_MAP = {
    MOTION_TYPE: [PRO, ANTI, DASH, STATIC],
    COLOR: [BLUE, RED],
    LEAD_STATE: [LEADING, TRAILING],
}


class AttrPanel(QFrame):
    def __init__(self, filter_tab: "FilterTab", attribute_type) -> None:
        super().__init__()
        self.filter_tab = filter_tab
        self.attribute_type = attribute_type
        self.boxes = self._create_boxes(attribute_type)
        self.setup_layouts()

    def _create_boxes(self, attribute_type) -> List[AttrBox]:
        attributes = []
        if attribute_type == MOTION_TYPE and self.filter_tab.letter_type is not None:
            attributes = letter_type_motion_type_map[self.filter_tab.letter_type]
        elif attribute_type == COLOR:
            attributes = [BLUE, RED]
        elif attribute_type == LEAD_STATE:
            attributes = [LEADING, TRAILING]

        return [AttrBox(self, attribute_type, attribute) for attribute in attributes]

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for box in self.boxes:
            self.layout.addWidget(box)

    def reset_turns(self) -> None:
        for box in self.boxes:
            box.turns_widget.turns_display_manager.turns_display.setText("0")
            if hasattr(box, "header_widget"):
                for button in (
                    box.rot_dir_button_manager.vtg_dir_buttons
                    + box.rot_dir_button_manager.prop_rot_dir_buttons
                ):
                    button.unpress()
        for pictograph in self.filter_tab.scroll_area.pictographs.values():
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
