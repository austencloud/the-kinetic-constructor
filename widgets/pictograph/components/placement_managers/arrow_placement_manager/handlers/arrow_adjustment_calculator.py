import re
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Optional, Tuple

from utilities.TypeChecking.letter_lists import (
    Type1_hybrid_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    non_hybrid_letters,
)
from .directional_tuple_generator import DirectionalTupleGenerator

if TYPE_CHECKING:
    from ..arrow_placement_manager import ArrowPlacementManager


class ArrowAdjustmentCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.pm = placement_manager

    def get_adjustment(self, arrow: Arrow) -> QPointF:
        turns_tuple = self.pm.key_generator.generate_turns_tuple(
            self.pm.pictograph.letter
        )

        special_placements = (
            self.pm.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        if self.pm.pictograph.letter in special_placements:
            special_adjustment = (
                self.pm.adjustment_calculator.get_adjustment_for_letter(
                    self.pm.pictograph.letter, arrow, turns_tuple
                )
            )
            (
                x,
                y,
            ) = special_adjustment or self.pm.default_positioner.get_default_adjustment(
                arrow
            )
        else:
            x, y = self.pm.default_positioner.get_default_adjustment(arrow)

        directional_generator = DirectionalTupleGenerator(
            arrow.motion, arrow.pictograph.get.other_motion(arrow.motion)
        )
        directional_adjustments = directional_generator.generate_directional_tuples(
            x, y
        )
        quadrant_index = self.pm.quadrant_index_handler.get_quadrant_index(arrow)
        return QPointF(*directional_adjustments[quadrant_index])

    def _find_special_rotation(self, turn_data: Dict) -> Optional[Dict]:
        for key, value in turn_data.items():
            if re.match(r"^(cw|ccw)_static$", key):
                return value
        return None

    def get_adjustment_for_letter(
        self, letter: str, arrow: Arrow, turns_tuple: str = None
    ) -> Optional[Tuple[int, int]]:
        if turns_tuple is None:
            turns_tuple = (
                self.pm.special_positioner.turns_tuple_generator.generate_turns_tuple(
                    letter
                )
            )
        self.special_placements: Dict[
            str, Dict
        ] = self.pm.pictograph.main_widget.special_placements

        letter_adjustments: Dict = self.special_placements.get(letter, {}).get(
            turns_tuple, {}
        )
        adjustment_map = {
            "S": letter_adjustments.get(arrow.motion.lead_state),
            "T": letter_adjustments.get(arrow.motion.lead_state),
            **{
                letter: letter_adjustments.get(arrow.motion.motion_type)
                for letter in Type1_hybrid_letters
            },
            **{
                letter: letter_adjustments.get(arrow.color)
                for letter in non_hybrid_letters
                if letter not in ["S", "T"]
            },
            **{
                letter: letter_adjustments.get(arrow.motion.motion_type)
                for letter in Type2_letters + Type3_letters + Type4_letters
            },
        }

        return adjustment_map.get(letter)
