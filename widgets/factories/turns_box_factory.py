from typing import TYPE_CHECKING

from Enums.Enums import TurnsTabAttribute
from Enums.MotionAttributes import LeadStates, MotionType
from data.constants import BLUE, RED
from widgets.letterbook.letterbook_letter_button_frame.components.letterbook_turns_box import (
    LetterBookTurnsBox,
)


if TYPE_CHECKING:
    from widgets.letterbook_turns_panel import LetterBookTurnsPanel


class LetterBookTurnsBoxFactory:
    def __init__(self, turns_panel: "LetterBookTurnsPanel") -> None:
        self.turns_panel = turns_panel

    def create_boxes(self) -> list[LetterBookTurnsBox]:
        attributes = []
        if self.turns_panel.attribute_type == TurnsTabAttribute.MOTION_TYPE:
            return [
                LetterBookTurnsBox(
                    self.turns_panel, TurnsTabAttribute.MOTION_TYPE, motion_type
                )
                for motion_type in [
                    MotionType.PRO,
                    MotionType.ANTI,
                    MotionType.DASH,
                    MotionType.STATIC,
                ]
            ]
        elif self.turns_panel.attribute_type == TurnsTabAttribute.COLOR:
            attributes = [BLUE, RED]
        elif self.turns_panel.attribute_type == TurnsTabAttribute.LEAD_STATE:
            attributes = [LeadStates.LEADING, LeadStates.TRAILING]

        return [
            LetterBookTurnsBox(
                self.turns_panel, self.turns_panel.attribute_type, attribute
            )
            for attribute in attributes
        ]
