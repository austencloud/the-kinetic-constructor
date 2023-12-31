from objects.pictograph.position_engines.arrow_positioners.base_arrow_positioner import (
    BaseArrowPositioner,
)
from constants import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
)
from objects.arrow import Arrow
from PyQt6.QtCore import QPointF


class Type5ArrowPositioner(BaseArrowPositioner):
    def _reposition_Λ_dash(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_Λ_dash_adjustments(arrow)
            self._apply_dash_adjustment(arrow, adjustment)

    def _calculate_Λ_dash_adjustments(self, arrow: Arrow) -> QPointF:
        adjustments = {
            NORTH: QPointF(0, 45),
            EAST: QPointF(-45, 0),
            SOUTH: QPointF(0, -45),
            WEST: QPointF(45, 0),
        }
        return adjustments.get(arrow.loc)
