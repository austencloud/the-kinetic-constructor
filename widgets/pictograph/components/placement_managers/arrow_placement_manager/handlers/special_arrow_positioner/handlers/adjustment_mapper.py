from typing import TYPE_CHECKING, Tuple
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from ..special_arrow_positioner import SpecialArrowPositioner


class AdjustmentMapper:
    def __init__(self, positioner: "SpecialArrowPositioner") -> None:
        self.positioner = positioner

    def apply_adjustment_to_arrow(self, arrow: Arrow) -> None:
        tuple_generator = self.positioner.turns_tuple_generator
        adjustment_key = tuple_generator.generate_turns_tuple(arrow)
        adjustment = self.positioner.adjustment_calculator.calculate_turns_tuple(
            arrow, adjustment_key
        )

        if adjustment:
            self._apply_adjustment(arrow, adjustment)

    def _apply_adjustment(self, arrow: Arrow, adjustment: Tuple[int, int]) -> None:
        new_x = arrow.x() + adjustment[0]
        new_y = arrow.y() + adjustment[1]
        arrow.setPos(new_x, new_y)
