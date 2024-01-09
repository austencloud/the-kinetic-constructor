from typing import TYPE_CHECKING, Callable, Dict
from utilities.TypeChecking.TypeChecking import Locations
from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowLocationManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.location_resolvers = {
            PRO: self.get_shift_location,
            ANTI: self.get_shift_location,
            FLOAT: self.get_shift_location,
            DASH: self.resolve_dash_location,
            STATIC: self.get_static_location,
        }

    def update_location(self) -> None:
        if not self.arrow.is_ghost and self.arrow.ghost and not self.arrow.loc:
            self.arrow.loc = self.get_arrow_location()
            self.arrow.ghost.loc = self.arrow.loc

    def get_arrow_location(self) -> Locations:
        resolve_location: Callable = self.location_resolvers.get(self.arrow.motion_type)
        return resolve_location()

    def get_shift_location(self) -> Locations:
        direction_pairs = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
        }
        return direction_pairs.get(
            frozenset({self.arrow.motion.start_loc, self.arrow.motion.end_loc})
        )

    def resolve_dash_location(self) -> Locations:
        return (
            self._dash_location_zero_turns()
            if self.arrow.motion.turns == 0
            else self._dash_location_non_zero_turns()
        )

    def _dash_location_zero_turns(self) -> Locations:
        other_motion = (
            self.arrow.scene.motions[RED]
            if self.arrow.color == BLUE
            else self.arrow.scene.motions[BLUE]
        )
        if self.arrow.scene.letter in ["Φ", "Ψ"]:
            dash_map = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
            return dash_map.get(other_motion.arrow.loc, self._default_dash_location())
        elif self.arrow.scene.letter in ["Λ-"]:
            loc_map = {
                ((NORTH, SOUTH), (EAST, WEST)): EAST,
                ((EAST, WEST), (NORTH, SOUTH)): NORTH,
                ((NORTH, SOUTH), (WEST, EAST)): WEST,
                ((WEST, EAST), (NORTH, SOUTH)): NORTH,
                ((SOUTH, NORTH), (EAST, WEST)): EAST,
                ((EAST, WEST), (SOUTH, NORTH)): SOUTH,
                ((SOUTH, NORTH), (WEST, EAST)): WEST,
                ((WEST, EAST), (SOUTH, NORTH)): SOUTH,
            }
            arrow_location = loc_map.get(
            (
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                (other_motion.start_loc, other_motion.end_loc),
            ))
            return arrow_location
            

    def _dash_location_non_zero_turns(self) -> Locations:
        rot_map = {
            CLOCKWISE: {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH},
            COUNTER_CLOCKWISE: {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH},
        }
        return rot_map[self.arrow.motion.prop_rot_dir][self.arrow.motion.start_loc]

    def get_opposite_arrow(self) -> "Arrow":
        return self.arrow.scene.arrows[RED if self.arrow.color == BLUE else BLUE]

    def _default_dash_location(self) -> Locations:
        color_map = {
            BLUE: {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH},
            RED: {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH},
        }
        return color_map[self.arrow.color][self.arrow.motion.start_loc]

    def get_static_location(self) -> Locations:
        return self.arrow.motion.start_loc
