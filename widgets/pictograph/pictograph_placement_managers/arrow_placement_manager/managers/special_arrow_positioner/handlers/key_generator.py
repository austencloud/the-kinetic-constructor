from typing import TYPE_CHECKING, Dict

from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from ..special_arrow_positioner import SpecialArrowPositioner


class KeyGenerator:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def determine_key(self, arrow: "Arrow") -> str:
        if self.positioner.pictograph.letter in ["S", "T"]:
            return arrow.motion.lead_state
        elif self.positioner.pictograph.letter in Type1_non_hybrid_letters:
            return arrow.color
        else:
            return arrow.motion.motion_type

    def _get_other_key(self, arrow: "Arrow") -> str:
        other_arrow = (
            self.positioner.pictograph.blue_arrow
            if arrow == self.positioner.pictograph.red_arrow
            else self.positioner.pictograph.red_arrow
        )
        if self.positioner.pictograph.letter in ["S", "T"]:
            return other_arrow.motion.lead_state
        elif self.positioner.pictograph.letter in Type1_non_hybrid_letters:
            return other_arrow.color
        else:
            return other_arrow.motion.motion_type

    def generate_adjustment_key(self, arrow: "Arrow") -> str:
        key = self.determine_key(arrow)
        other_key = self._get_other_key(arrow)
        return f"{key}({other_key})"
