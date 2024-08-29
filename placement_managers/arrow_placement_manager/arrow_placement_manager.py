from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING
from .components.arrow_adjustment_calculator import ArrowAdjustmentCalculator
from .components.arrow_initial_pos_calculator import ArrowInitialPosCalculator

from .components.default_arrow_positioner import DefaultArrowPositioner
from .components.quadrant_index_handler import QuadrantIndexHandler
from .components.special_arrow_positioner.special_arrow_positioner import (
    SpecialArrowPositioner,
)


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class ArrowPlacementManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph

        # Positioners
        self.default_positioner = DefaultArrowPositioner(self)
        self.special_positioner = SpecialArrowPositioner(self)

        self.initial_pos_calculator = ArrowInitialPosCalculator(self)
        self.adjustment_calculator = ArrowAdjustmentCalculator(self)
        self.quadrant_index_handler = QuadrantIndexHandler(self)

    def update_arrow_placements(self) -> None:
        for arrow in self.pictograph.arrows.values():
            self.update_arrow_position(arrow)

    def update_arrow_position(self, arrow: Arrow) -> None:
        initial_pos = self.initial_pos_calculator.get_initial_pos(arrow)
        adjustment = self.adjustment_calculator.get_adjustment(arrow)
        new_pos = initial_pos + adjustment - arrow.boundingRect().center()
        arrow.setPos(new_pos)
        arrow.rot_angle_manager.update_rotation()
