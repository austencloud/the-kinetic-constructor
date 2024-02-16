from typing import TYPE_CHECKING

from Enums.Enums import TurnsTabAttributeType
from Enums.MotionAttributes import Colors, LeadStates, MotionTypes
from widgets.turns_box.turns_box import TurnsBox


if TYPE_CHECKING:
    from widgets.turns_panel import TurnsPanel


class TurnsBoxFactory:
    def __init__(self, turns_panel: "TurnsPanel") -> None:
        self.turns_panel = turns_panel

    def create_boxes(self) -> list[TurnsBox]:
        attributes = []
        if self.turns_panel.attribute_type == TurnsTabAttributeType.MOTION_TYPE:
            return [
                TurnsBox(
                    self.turns_panel, TurnsTabAttributeType.MOTION_TYPE, motion_type
                )
                for motion_type in [
                    MotionTypes.PRO,
                    MotionTypes.ANTI,
                    MotionTypes.DASH,
                    MotionTypes.STATIC,
                ]
            ]
        elif self.turns_panel.attribute_type == TurnsTabAttributeType.COLOR:
            attributes = [Colors.BLUE, Colors.RED]
        elif self.turns_panel.attribute_type == TurnsTabAttributeType.LEAD_STATE:
            attributes = [LeadStates.LEADING, LeadStates.TRAILING]

        return [
            TurnsBox(self.turns_panel, self.turns_panel.attribute_type, attribute)
            for attribute in attributes
        ]
