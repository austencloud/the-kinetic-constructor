from PyQt6.QtCore import QPointF
from numpy import place
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING

from widgets.pictograph.components.placement_managers.arrow_placement_manager.arrow_adjustment_calculator import ArrowAdjustmentCalculator
from .handlers.turns_tuple_generator import TurnsTupleGenerator
from .handlers.arrow_initial_pos_calculator import ArrowInitialPosCalculator
from .handlers.directional_tuple_generator import DirectionalTupleGenerator
from .handlers.quadrant_index_handler import QuadrantIndexHandler
from .handlers.default_arrow_positioner import DefaultArrowPositioner
from .handlers.special_arrow_positioner.special_arrow_positioner import (
    SpecialArrowPositioner,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class ArrowPlacementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultArrowPositioner(self)
        self.special_positioner = SpecialArrowPositioner(self)

        self.initial_pos_calculator = ArrowInitialPosCalculator(self)
        self.adjustment_calculator = ArrowAdjustmentCalculator(self)
        self.key_generator = TurnsTupleGenerator(self)
        self.quadrant_index_handler = QuadrantIndexHandler(self)

    def update_arrow_positions(self) -> None:
        self.letter = self.pictograph.letter
        for arrow in self.pictograph.arrows.values():
            self.update_arrow_position(arrow)
            self.update_arrow_position(arrow.ghost)

    def update_arrow_position(self, arrow: Arrow) -> None:
        initial_pos = self.initial_pos_calculator.get_initial_pos(arrow)
        adjustment = self.adjustment_calculator.get_adjustment(arrow)
        new_pos = initial_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        arrow.rot_angle_calculator.update_rotation()


