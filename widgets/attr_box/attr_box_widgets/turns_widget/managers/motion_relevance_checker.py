from typing import TYPE_CHECKING
from constants import COLOR, LEAD_STATE, MOTION_TYPE

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion


class MotionRelevanceChecker:
    def __init__(self, attr_box: "AttrBox") -> None:
        self.attr_box = attr_box

    def is_motion_relevant(self, motion: "Motion") -> bool:
        attr_type = self.attr_box.attribute_type
        is_same_letter_type = (
            self.attr_box.attr_panel.filter_tab.section.letter_type
            == motion.pictograph.letter.type
        )

        if not is_same_letter_type:
            return False

        if attr_type == MOTION_TYPE:
            return motion.motion_type == self.attr_box.motion_type
        elif attr_type == COLOR:
            return motion.color == self.attr_box.color
        elif attr_type == LEAD_STATE:
            return motion.lead_state == self.attr_box.lead_state

        return False  # Default case if none of the conditions match
