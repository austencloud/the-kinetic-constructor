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
    DOWNRIGHT,
    UPLEFT,
    DOWNLEFT,
    UPRIGHT,
)
from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from placement_managers.prop_placement_manager.handlers.beta_prop_positioner import BetaPropPositioner
    from ..prop_placement_manager import PropPlacementManager


class BetaOffsetCalculator:
    def __init__(self, beta_positioner: "BetaPropPositioner") -> None:
        self.position_offsets_cache: dict[PropType, dict[tuple[str, str], QPointF]] = {}
        self.beta_positioner = beta_positioner
        self.pictograph = beta_positioner.pictograph

    def calculate_new_position_with_offset(
        self, current_position: QPointF, direction: str
    ) -> QPointF:
        prop_type_map = {
            PropType.Club: 60,
            PropType.Eightrings: 60,
            PropType.BigEightRings: 60,
            PropType.Doublestar: 50,
            PropType.Bigdoublestar: 50,
        }
        prop_type = self.beta_positioner.pictograph.prop_type
        self.beta_offset = (
            self.beta_positioner.pictograph.width()
            / prop_type_map.get(prop_type, 45)
        )

        # Update offset_map to include diagonal directions
        offset_map = {
            LEFT: QPointF(-self.beta_offset, 0),
            RIGHT: QPointF(self.beta_offset, 0),
            UP: QPointF(0, -self.beta_offset),
            DOWN: QPointF(0, self.beta_offset),
            # Diagonal directions
            DOWNRIGHT: QPointF(self.beta_offset, self.beta_offset),
            UPLEFT: QPointF(-self.beta_offset, -self.beta_offset),
            DOWNLEFT: QPointF(-self.beta_offset, self.beta_offset),
            UPRIGHT: QPointF(self.beta_offset, -self.beta_offset),
        }

        # Get the corresponding offset for the direction, defaulting to no offset if not found
        offset = offset_map.get(direction, QPointF(0, 0))

        # Return the new position by applying the calculated offset to the current position
        return current_position + offset
