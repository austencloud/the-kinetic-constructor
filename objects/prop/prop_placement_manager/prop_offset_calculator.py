from constants import (
    IN,
    OUT,
    CLOCK,
    COUNTER,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Dict, Tuple
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Directions

if TYPE_CHECKING:
    from objects.prop.prop_placement_manager.prop_placement_manager import (
        PropPlacementManager,
    )


class PropOffsetCalculator:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.position_offsets_cache: Dict[Prop, Dict[Tuple[str, str], QPointF]] = {}
        self.prop_placement_manager = prop_placement_manager

    def get_or_calculate_offsets(self, prop: Prop) -> Dict[Tuple[str, str], QPointF]:
        if prop not in self.position_offsets_cache:
            self.position_offsets_cache[prop] = self.calculate_offsets(prop)
        return self.position_offsets_cache[prop]

    def calculate_offsets(self, prop: Prop) -> Dict[Tuple[str, str], QPointF]:
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()

        x = prop_width / 2
        y = prop_length / 2

        return {
            (IN, NORTH): QPointF(x, -y),
            (IN, SOUTH): QPointF(-x, y),
            (IN, EAST): QPointF(y, x),
            (IN, WEST): QPointF(-y, -x),
            (OUT, NORTH): QPointF(-x, y),
            (OUT, SOUTH): QPointF(x, -y),
            (OUT, EAST): QPointF(-y, -x),
            (OUT, WEST): QPointF(y, x),
            (CLOCK, NORTH): QPointF(-y, -x),
            (CLOCK, SOUTH): QPointF(y, x),
            (CLOCK, EAST): QPointF(x, -y),
            (CLOCK, WEST): QPointF(-x, y),
            (COUNTER, NORTH): QPointF(y, x),
            (COUNTER, SOUTH): QPointF(-y, -x),
            (COUNTER, EAST): QPointF(-x, y),
            (COUNTER, WEST): QPointF(x, -y),
        }

    def calculate_new_position_with_offset(
        self, current_position: QPointF, direction: Directions
    ) -> QPointF:
        self.beta_offset = self.prop_placement_manager.pictograph.width() / 38

        offset_map = {
            LEFT: QPointF(-self.beta_offset, 0),
            RIGHT: QPointF(self.beta_offset, 0),
            UP: QPointF(0, -self.beta_offset),
            DOWN: QPointF(0, self.beta_offset),
        }
        offset = offset_map.get(direction, QPointF(0, 0))
        return current_position + offset