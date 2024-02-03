from typing import TYPE_CHECKING, Literal
from objects.arrow.arrow import Arrow
from constants import (
    DIAMOND,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    NORTH,
    EAST,
    SOUTH,
    WEST,
    PRO,
    ANTI,
    STATIC,
    DASH,
)
from utilities.TypeChecking.MotionAttributes import Locations

if TYPE_CHECKING:
    from ...arrow_placement_manager.arrow_placement_manager import ArrowPlacementManager


class QuadrantIndexHandler:
    def __init__(self, placement_manager: "ArrowPlacementManager") -> None:
        self.grid_mode = placement_manager.pictograph.main_widget.grid_mode

    def get_quadrant_index(self, arrow: Arrow) -> Literal[0, 1, 2, 3]:
        if self.grid_mode == DIAMOND:
            if arrow.motion.motion_type in [PRO, ANTI]:
                return self._diamond_shift_quadrant_index(arrow.loc)
            elif arrow.motion.motion_type in [STATIC, DASH]:
                return self._diamond_static_dash_quadrant_index(arrow.loc)
        return 0

    def _diamond_shift_quadrant_index(self, location: Locations) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTHEAST: 0,
            SOUTHEAST: 1,
            SOUTHWEST: 2,
            NORTHWEST: 3,
        }
        return location_to_index.get(location, 0)

    def _diamond_static_dash_quadrant_index(
        self, location: Locations
    ) -> Literal[0, 1, 2, 3]:
        location_to_index = {
            NORTH: 0,
            EAST: 1,
            SOUTH: 2,
            WEST: 3,
        }
        return location_to_index.get(location, 0)
