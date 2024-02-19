from typing import TYPE_CHECKING
from Enums.Enums import LetterType, TurnsTabAttribute


if TYPE_CHECKING:
    from widgets.turns_box.codex_turns_box import CodexTurnsBox
    from objects.motion.motion import Motion


class MotionRelevanceChecker:
    def __init__(self, turns_box: "CodexTurnsBox") -> None:
        self.turns_box = turns_box

    def is_motion_relevant(self, motion: "Motion") -> bool:
        attr_type = self.turns_box.attribute_type
        is_same_letter_type = (
            self.turns_box.turns_panel.turns_tab.section.letter_type
            == LetterType.get_letter_type(motion.pictograph.letter)
        )

        if not is_same_letter_type:
            return False

        if attr_type == TurnsTabAttribute.MOTION_TYPE:
            return motion.motion_type == self.turns_box.motion_type.value
        elif attr_type == TurnsTabAttribute.COLOR:
            return motion.color == self.turns_box.color
        elif attr_type == TurnsTabAttribute.LEAD_STATE:
            return motion.lead_state == self.turns_box.lead_state

        return False  # Default case if none of the conditions match
