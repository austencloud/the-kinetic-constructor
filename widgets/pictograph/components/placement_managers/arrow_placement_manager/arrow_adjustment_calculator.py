from PyQt6.QtCore import QPointF
from numpy import place
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

from .handlers.turns_tuple_generator import TurnsTupleGenerator
from .handlers.arrow_initial_pos_calculator import ArrowInitialPosCalculator
from .handlers.directional_tuple_generator import DirectionalTupleGenerator
from .handlers.quadrant_index_handler import QuadrantIndexHandler
from .handlers.default_arrow_positioner import DefaultArrowPositioner
from .handlers.special_arrow_positioner.special_arrow_positioner import (
    SpecialArrowPositioner,
)

if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.arrow_placement_manager.arrow_placement_manager import (
        ArrowPlacementManager,
    )


class ArrowAdjustmentCalculator:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.pm = placement_manager

    def get_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_key = self.pm.key_generator.generate_turns_tuple(
            self.pm.pictograph.letter
        )
        self.pm.special_positioner.special_placements = (
            self.pm.special_positioner.data_loader.load_placements()
        )

        if self.pm.pictograph.letter in self.pm.special_positioner.special_placements:
            special_adjustment = self.pm.special_positioner.adjustment_calculator.get_adjustment_for_letter(
                self.pm.pictograph.letter, arrow, adjustment_key
            )
            if special_adjustment:
                x, y = special_adjustment
            else:
                x, y = self.pm.default_positioner.get_default_adjustment(arrow)
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
