from typing import TYPE_CHECKING

from Enums.Enums import TurnsTabAttribute
from Enums.MotionAttributes import LeadStates, MotionType
from widgets.codex.codex_letter_button_frame.components.codex_turns_box import (
    CodexTurnsBox,
)


if TYPE_CHECKING:
    from widgets.codex_turns_panel import CodexTurnsBoxPanel


class CodexTurnsBoxFactory:
    def __init__(self, turns_panel: "CodexTurnsBoxPanel") -> None:
        self.turns_panel = turns_panel

    def create_boxes(self) -> list[CodexTurnsBox]:
        attributes = []
        if self.turns_panel.attribute_type == TurnsTabAttribute.MOTION_TYPE:
            return [
                CodexTurnsBox(
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
            CodexTurnsBox(self.turns_panel, self.turns_panel.attribute_type, attribute)
            for attribute in attributes
        ]
