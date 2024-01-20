from typing import TYPE_CHECKING, List

from constants import (
    ANTI,
    BLUE,
    COLOR,
    DASH,
    LEAD_STATE,
    LEADING,
    MOTION_TYPE,
    PRO,
    RED,
    STATIC,
    TRAILING,
)
from utilities.TypeChecking.MotionAttributes import MotionTypes
from utilities.TypeChecking.letter_lists import pro_letters, anti_letters
from widgets.attr_box.attr_box import AttrBox


if TYPE_CHECKING:
    from widgets.attr_panel import AttrPanel


class AttrBoxFactory:
    def __init__(self, attr_panel: "AttrPanel") -> None:
        self.attr_panel = attr_panel

    def create_boxes(self) -> List[AttrBox]:
        attributes = []
        if self.attr_panel.attribute_type == MOTION_TYPE:
            return [AttrBox(self.attr_panel, MOTION_TYPE, motion_type)
                    for motion_type in [PRO, ANTI, DASH, STATIC]]
        elif self.attr_panel.attribute_type == COLOR:
            attributes = [BLUE, RED]
        elif self.attr_panel.attribute_type == LEAD_STATE:
            attributes = [LEADING, TRAILING]

        return [AttrBox(self.attr_panel, self.attr_panel.attribute_type, attribute)
                for attribute in attributes]

