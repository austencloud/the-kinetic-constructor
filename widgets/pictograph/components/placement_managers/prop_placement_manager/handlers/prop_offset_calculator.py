from Enums.PropTypes import PropType
from data.constants import (
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
from typing import TYPE_CHECKING
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from ..prop_placement_manager import PropPlacementManager


class PropOffsetCalculator:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.position_offsets_cache: dict[PropType, dict[tuple[str, str], QPointF]] = {}
        self.prop_placement_manager = prop_placement_manager
        self.pictograph = prop_placement_manager.pictograph

    def get_or_calculate_offsets(self, prop: Prop) -> dict[tuple[str, str], QPointF]:
        if prop.prop_type not in self.position_offsets_cache:
            self.position_offsets_cache[prop.prop_type] = self.calculate_offsets(prop)
        return self.position_offsets_cache[prop.prop_type]

    def calculate_offsets(self, prop: Prop) -> dict[tuple[str, str], QPointF]:
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()

        x = prop_width / 2
        y = prop_length / 2

        non_hand_offsets = {
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

        hand_offsets = {
            (IN, NORTH): QPointF(-y, -x),
            (IN, SOUTH): QPointF(-y, -x),
            (IN, EAST): QPointF(-y, -x),
            (IN, WEST): QPointF(-y, -x),
            (OUT, NORTH): QPointF(-y, -x),
            (OUT, SOUTH): QPointF(-y, -x),
            (OUT, EAST): QPointF(-y, -x),
            (OUT, WEST): QPointF(-y, -x),
            (CLOCK, NORTH): QPointF(-y, -x),
            (CLOCK, SOUTH): QPointF(-y, -x),
            (CLOCK, EAST): QPointF(-y, -x),
            (CLOCK, WEST): QPointF(-y, -x),
            (COUNTER, NORTH): QPointF(-y, -x),
            (COUNTER, SOUTH): QPointF(-y, -x),
            (COUNTER, EAST): QPointF(-y, -x),
            (COUNTER, WEST): QPointF(-y, -x),
        }


        return non_hand_offsets if prop.prop_type != PropType.Hand else hand_offsets

    def calculate_new_position_with_offset(
        self, current_position: QPointF, direction: str
    ) -> QPointF:
        prop_type_map = {
            PropType.Club: 60,
            PropType.EightRings: 60,
            PropType.BigEightRings: 60,
            PropType.DoubleStar: 50,
            PropType.BigDoubleStar: 50,
        }
        prop_type = self.prop_placement_manager.pictograph.prop_type
        self.beta_offset = (
            self.prop_placement_manager.pictograph.width()
            / prop_type_map.get(prop_type, 45)
        )

        offset_map = {
            LEFT: QPointF(-self.beta_offset, 0),
            RIGHT: QPointF(self.beta_offset, 0),
            UP: QPointF(0, -self.beta_offset),
            DOWN: QPointF(0, self.beta_offset),
        }
        offset = offset_map.get(direction, QPointF(0, 0))
        return current_position + offset
