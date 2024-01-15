from typing import TYPE_CHECKING, Dict, List, Literal, Set, Union
from constants import (
    BLUE,
    BLUE_END_LOC,
    BLUE_END_ORI,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    END_POS,
    LETTER,
    MOTION_TYPE,
    NO_ROT,
    OPP,
    PROP_ROT_DIR,
    RED,
    RED_END_LOC,
    RED_END_ORI,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    SAME,
    START_POS,
    STATIC,
    TURNS,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.letter_lists import all_letters
from ...filter_frame.attr_box.color_attr_box import ColorAttrBox
from ...filter_frame.attr_box.lead_state_attr_box import LeadStateAttrBox
from ...filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox
from .ig_pictograph import IGPictograph
from ...pictograph_scroll_area.pictograph_scroll_area import PictographScrollArea
from constants import IG_PICTOGRAPH
from utilities.TypeChecking.TypeChecking import (
    Letters,
    Turns,
    Orientations,
    VtgDirections,
)
from PyQt6.QtCore import QTimer

if TYPE_CHECKING:
    from ...parent_tab.parent_tab import IGTab
    from ...main_widget import MainWidget


class FilterManagement:
    def __init__(self, parent_tab: "IGTab"):
        self.parent_tab = parent_tab

    def filter_pictographs(self, pictograph_dicts: List[Dict]) -> List[Dict]:
        return [
            pictograph_dict
            for pictograph_dict in pictograph_dicts
            if self.pictograph_matches_filters(pictograph_dict)
        ]

    def pictograph_matches_filters(self, pictograph_dict: Dict) -> bool:
        for filter_key, filter_value in self.filters.items():
            if filter_value in ["0", "1", "2", "3"]:
                filter_value = int(filter_value)
            elif filter_value in ["0.5", "1.5", "2.5"]:
                filter_value = float(filter_value)
            if filter_value != "":
                if pictograph_dict.get(filter_key) != filter_value:
                    return False
        return True
