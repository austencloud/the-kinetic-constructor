from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from .managers.adjustment_key_generator import AdjustmentKeyGenerator
from .managers.arrow_initial_pos_calculator import ArrowInitialPosCalculator
from .managers.directional_tuple_generator import DirectionalTupleGenerator
from .managers.quadrant_index_handler import QuadrantIndexHandler
from .managers.default_arrow_positioner import DefaultArrowPositioner
from .managers.special_arrow_positioner import SpecialArrowPositioner

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class ArrowPlacementManager:
    """Manages the placement of main arrows within the pictograph based on specific rules and letter types."""

    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.default_positioner = DefaultArrowPositioner(pictograph)
        self.special_positioner = SpecialArrowPositioner(pictograph)
        self.initial_pos_calculator = ArrowInitialPosCalculator(pictograph)
        self.key_generator = AdjustmentKeyGenerator(pictograph)
        self.quadrant_index_handler = QuadrantIndexHandler(pictograph)

    def update_arrow_placement(self) -> None:
        """Update the placement of all arrows."""
        self.letter = self.pictograph.letter
        for arrow in self.pictograph.arrows.values():
            if arrow.loc:
                self.update_arrow_position(arrow)

    def update_arrow_position(self, arrow: Arrow) -> None:
        initial_pos = self.initial_pos_calculator.get_initial_pos(arrow)
        adjustment = self.get_adjustment(arrow)
        new_pos = initial_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        arrow.rot_angle_calculator.update_rotation()

    def get_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_key = self.key_generator.generate(self.pictograph.letter)
        self.special_positioner.special_placements = (
            self.special_positioner._load_placements()
        )

        if self.letter in self.special_positioner.special_placements:
            special_adjustment = self.special_positioner.get_adjustment_for_letter(
                self.letter, arrow, adjustment_key
            )
            if special_adjustment:
                x, y = special_adjustment
            else:
                x, y = self.default_positioner.get_default_adjustment(arrow)
        else:
            x, y = self.default_positioner.get_default_adjustment(arrow)
        directional_generator = DirectionalTupleGenerator(
            arrow.motion, arrow.pictograph.get.other_motion(arrow.motion)
        )
        directional_adjustments = directional_generator.generate_directional_tuples(
            x, y
        )
        quadrant_index = self.quadrant_index_handler.get_quadrant_index(arrow)
        return QPointF(*directional_adjustments[quadrant_index])
