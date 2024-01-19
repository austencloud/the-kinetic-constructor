from PyQt6.QtCore import QPointF
from numpy import place
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from .managers.turns_tuple_generator import TurnsTupleGenerator
from .managers.arrow_initial_pos_calculator import ArrowInitialPosCalculator
from .managers.directional_tuple_generator import DirectionalTupleGenerator
from .managers.quadrant_index_handler import QuadrantIndexHandler
from .managers.default_arrow_positioner import DefaultArrowPositioner
from .managers.special_arrow_positioner.special_arrow_positioner import (
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
