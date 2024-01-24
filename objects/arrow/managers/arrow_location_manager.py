from typing import TYPE_CHECKING, Callable
from utilities.TypeChecking.letter_lists import Type3_letters, Type4_letters
from utilities.TypeChecking.TypeChecking import Locations
from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowLocationCalculator:
    def __init__(self, arrow: "Arrow") -> None:
        self.a = arrow
        self.location_resolvers = {
            PRO: self.get_shift_location,
            ANTI: self.get_shift_location,
            FLOAT: self.get_shift_location,
            DASH: self.get_dash_location,
            STATIC: self.get_static_location,
        }

    def update_location(self, new_location: Locations = None) -> None:
        if new_location:
            self.a.loc = new_location
            self.a.ghost.loc = new_location
        elif not self.a.is_ghost and self.a.ghost:
            self.a.loc = self.get_arrow_location()
            self.a.ghost.loc = self.a.loc

    def get_arrow_location(self) -> Locations:
        resolve_location: Callable = self.location_resolvers.get(
            self.a.motion.motion_type
        )
        if resolve_location:
            return resolve_location()

    def get_shift_location(self) -> Locations:
        direction_pairs = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
        }
        return direction_pairs.get(
            frozenset({self.a.motion.start_loc, self.a.motion.end_loc})
        )

    def get_dash_location(self) -> Locations:
        if str(self.a.scene.letter) in Type3_letters and self.a.motion.turns == 0:
            return self._zero_turns_type_3_dash_location()
        return (
            self._dash_location_zero_turns()
            if self.a.motion.turns == 0
            else self._dash_location_non_zero_turns()
        )

    def _dash_location_zero_turns(self) -> Locations:
        other_motion = self.a.scene.get.other_motion(self.a.motion)
        letter_str = str(self.a.scene.letter)

        if letter_str in Type3_letters or letter_str in Type4_letters:
            return self._default_dash_location()

        elif letter_str in ["Λ-"]:
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
                    (self.a.motion.start_loc, self.a.motion.end_loc),
                    (other_motion.start_loc, other_motion.end_loc),
                )
            )
            return arrow_location

    def _dash_location_non_zero_turns(self) -> Locations:
        loc_map = {
            CLOCKWISE: {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH},
            COUNTER_CLOCKWISE: {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH},
        }
        return loc_map[self.a.motion.prop_rot_dir][self.a.motion.start_loc]

    def _zero_turns_type_3_dash_location(self) -> Locations:
        shift_motion = (
            self.a.scene.red_motion
            if self.a.scene.red_motion.motion_type in [PRO, ANTI, FLOAT]
            else self.a.scene.blue_motion
        )
        dash_motion = (
            self.a.scene.red_motion
            if self.a.scene.red_motion.motion_type == DASH
            else self.a.scene.blue_motion
        )
        if not shift_motion.arrow.loc:
            shift_motion.arrow.loc = (
                shift_motion.arrow.location_calculator.get_arrow_location()
            )
        dash_location_map = {
            (NORTH, NORTHWEST): EAST,
            (NORTH, NORTHEAST): WEST,
            (NORTH, SOUTHEAST): WEST,
            (NORTH, SOUTHWEST): EAST,
            (EAST, NORTHWEST): SOUTH,
            (EAST, NORTHEAST): SOUTH,
            (EAST, SOUTHEAST): NORTH,
            (EAST, SOUTHWEST): NORTH,
            (SOUTH, NORTHWEST): EAST,
            (SOUTH, NORTHEAST): WEST,
            (SOUTH, SOUTHEAST): WEST,
            (SOUTH, SOUTHWEST): EAST,
            (WEST, NORTHWEST): SOUTH,
            (WEST, NORTHEAST): SOUTH,
            (WEST, SOUTHEAST): NORTH,
            (WEST, SOUTHWEST): NORTH,
        }
        dash_location = dash_location_map.get(
            (dash_motion.start_loc, shift_motion.arrow.loc)
        )
        return dash_location

    def get_opposite_arrow(self) -> "Arrow":
        return self.a.scene.arrows[RED if self.a.color == BLUE else BLUE]

    def _default_dash_location(self) -> Locations:
        location_map = {
            (NORTH, SOUTH): WEST,
            (EAST, WEST): SOUTH,
            (SOUTH, NORTH): EAST,
            (WEST, EAST): NORTH,
        }
        return location_map.get((self.a.motion.start_loc, self.a.motion.end_loc))

    def get_static_location(self) -> Locations:
        return self.a.motion.start_loc
