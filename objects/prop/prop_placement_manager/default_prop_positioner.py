from PyQt6.QtCore import QPointF
from typing import TYPE_CHECKING, Dict
from constants import *
from objects.prop.prop import Prop


if TYPE_CHECKING:
    from objects.prop.prop_placement_manager.prop_placement_manager import (
        PropPlacementManager,
    )


class DefaultPropPositioner:
    def __init__(self, prop_placement_manager: "PropPlacementManager") -> None:
        self.pictograph = prop_placement_manager.pictograph
        self.prop_placement_manager = prop_placement_manager
        self.location_points_cache = {}

    def set_prop_to_default_loc(self, prop: Prop, strict: bool = False) -> None:
        position_offsets = (
            self.prop_placement_manager.offset_calculator.get_or_calculate_offsets(prop)
        )
        key = (prop.ori, prop.loc)
        offset = position_offsets.get(key)
        prop.setTransformOriginPoint(0, 0)

        if self.pictograph.grid.grid_mode == DIAMOND:
            location_points = self.get_location_points(strict, DIAMOND)
        elif self.pictograph.grid.grid_mode == BOX:
            location_points = self.get_location_points(strict, BOX)

        for location, location_point in location_points.items():
            if prop.loc == location[0]:
                prop.setPos(location_point + offset)
                return

    def get_location_points(self, strict: bool, grid_mode: str) -> Dict[str, QPointF]:
        strict_key = "strict" if strict else "normal"
        location_points = self.pictograph.grid.circle_coordinates_cache["hand_points"][
            grid_mode
        ][strict_key]
        return location_points
