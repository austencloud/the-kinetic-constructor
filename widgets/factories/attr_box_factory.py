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
from widgets.turns_box.turns_box import TurnsBox


if TYPE_CHECKING:
    from widgets.turns_panel import TurnsPanel


class TurnsBoxFactory:
    def __init__(self, turns_panel: "TurnsPanel") -> None:
        self.turns_panel = turns_panel

    def create_boxes(self) -> List[TurnsBox]:
        attributes = []
        if self.turns_panel.attribute_type == MOTION_TYPE:
            return [
                TurnsBox(self.turns_panel, MOTION_TYPE, motion_type)
                for motion_type in [PRO, ANTI, DASH, STATIC]
            ]
        elif self.turns_panel.attribute_type == COLOR:
            attributes = [BLUE, RED]
        elif self.turns_panel.attribute_type == LEAD_STATE:
            attributes = [LEADING, TRAILING]

        return [
            TurnsBox(self.turns_panel, self.turns_panel.attribute_type, attribute)
            for attribute in attributes
        ]
