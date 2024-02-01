from typing import TYPE_CHECKING
from constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow
from utilities.TypeChecking.letter_lists import non_hybrid_letters

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class MotionAttrKeyGenerator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def get_key(self, arrow: "Arrow") -> str:
        if self.positioner.pictograph.letter in ["S", "T"]:
            if arrow.motion.start_ori in [IN, OUT]:
                return f"{arrow.motion.lead_state}_from_layer1"
            elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                return f"{arrow.motion.lead_state}_from_layer2"
        elif arrow.pictograph.check.starts_from_mixed_orientation():
            if arrow.pictograph.check.has_hybrid_motions():
                if arrow.motion.start_ori in [IN, OUT]:
                    return f"{arrow.motion.motion_type}_from_layer1"
                elif arrow.motion.start_ori in [CLOCK, COUNTER]:
                    return f"{arrow.motion.motion_type}_from_layer2"
            else:
                return arrow.motion.color
        elif self.positioner.pictograph.letter in non_hybrid_letters:
            return arrow.color
        else:
            return arrow.motion.motion_type

