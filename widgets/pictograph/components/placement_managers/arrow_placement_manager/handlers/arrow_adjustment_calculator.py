from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
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
            special_adjustment = self.pm.special_positioner.adjustment_calculator.get_adjustment_for_letter(
                self.pm.pictograph.letter, arrow, turns_tuple
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
