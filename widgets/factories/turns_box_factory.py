from typing import TYPE_CHECKING

from Enums.Enums import TurnsTabAttribute
from Enums.MotionAttributes import Color, LeadStates, MotionType
from widgets.turns_box.turns_box import TurnsBox


if TYPE_CHECKING:
    from widgets.turns_panel import GraphEditorAdjustmentPanel


class TurnsBoxFactory:
    def __init__(self, turns_panel: "GraphEditorAdjustmentPanel") -> None:
        self.turns_panel = turns_panel

    def create_boxes(self) -> list[TurnsBox]:
        attributes = []
        if self.turns_panel.attribute_type == TurnsTabAttribute.MOTION_TYPE:
            return [
                TurnsBox(self.turns_panel, TurnsTabAttribute.MOTION_TYPE, motion_type)
                for motion_type in [
                    MotionType.PRO,
                    MotionType.ANTI,
                    MotionType.DASH,
                    MotionType.STATIC,
                ]
            ]
        elif self.turns_panel.attribute_type == TurnsTabAttribute.COLOR:
            attributes = [Color.BLUE, Color.RED]
        elif self.turns_panel.attribute_type == TurnsTabAttribute.LEAD_STATE:
            attributes = [LeadStates.LEADING, LeadStates.TRAILING]

        return [
            TurnsBox(self.turns_panel, self.turns_panel.attribute_type, attribute)
            for attribute in attributes
        ]
