from typing import TYPE_CHECKING, Callable
from objects.motion.motion import Motion
from utilities.TypeChecking.letter_lists import Type3_letters
from utilities.TypeChecking.TypeChecking import Locations
from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowLocationCalculator:
    def __init__(self, arrow: "Arrow") -> None:
        self.a = arrow
        self.pictograph = self.a.pictograph
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
        self.other_motion = self.pictograph.get.other_motion(self.a.motion)
        if self.a.pictograph.letter in ["Φ-", "Ψ-"]:
            return self._get_Φ_dash_Ψ_dash_location()
        elif self.a.motion.turns == 0:
            return self._dash_location_zero_turns()
        elif self.a.motion.turns != 0:
            return self._dash_location_non_zero_turns()

    def _dash_location_zero_turns(self) -> Locations:
        letter_str = str(self.pictograph.letter)
        if str(self.pictograph.letter) in Type3_letters and self.a.motion.turns == 0:
            return self._zero_turns_type_3_dash_location()
        elif letter_str in ["Λ", "Λ-"]:
            arrow_location = self._get_Λ_zero_turns_location()
            return arrow_location

        else:
            return self._default_zero_turns_dash_location()

    def _get_Λ_zero_turns_location(self) -> Locations:
        loc_map = {
            ((NORTH, SOUTH), WEST): EAST,
            ((EAST, WEST), SOUTH): NORTH,
            ((NORTH, SOUTH), EAST): WEST,
            ((WEST, EAST), SOUTH): NORTH,
            ((SOUTH, NORTH), WEST): EAST,
            ((EAST, WEST), NORTH): SOUTH,
            ((SOUTH, NORTH), EAST): WEST,
            ((WEST, EAST), NORTH): SOUTH,
        }
        arrow_location = loc_map.get(
            (
                (self.a.motion.start_loc, self.a.motion.end_loc),
                (self.other_motion.end_loc),
            )
        )

        return arrow_location

    def _dash_location_non_zero_turns(self, motion: Motion = None) -> Locations:
        motion = motion if motion else self.a.motion
        loc_map = {
            CLOCKWISE: {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH},
            COUNTER_CLOCKWISE: {NORTH: WEST, EAST: NORTH, SOUTH: EAST, WEST: SOUTH},
        }
        return loc_map[motion.prop_rot_dir][motion.start_loc]

    def _get_Φ_dash_Ψ_dash_location(self) -> Locations:
        self.other_motion = self.pictograph.get.other_motion(self.a.motion)
        if self.a.motion.turns == 0 and self.other_motion.turns == 0:
            location_map = {
                (RED, (NORTH, SOUTH)): EAST,
                (RED, (EAST, WEST)): NORTH,
                (RED, (SOUTH, NORTH)): EAST,
                (RED, (WEST, EAST)): NORTH,
                (BLUE, (NORTH, SOUTH)): WEST,
                (BLUE, (EAST, WEST)): SOUTH,
                (BLUE, (SOUTH, NORTH)): WEST,
                (BLUE, (WEST, EAST)): SOUTH,
            }
            arrow_location = location_map.get(
                (self.a.color, (self.a.motion.start_loc, self.a.motion.end_loc))
            )
            return arrow_location

        elif self.a.motion.turns == 0:
            return self.pictograph.get.opposite_location(
                self._dash_location_non_zero_turns(self.other_motion)
            )
        elif self.a.motion.turns != 0:
            return self._dash_location_non_zero_turns(self.a.motion)

    def _zero_turns_type_3_dash_location(self) -> Locations:
        shift_motion = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.motion_type in [PRO, ANTI, FLOAT]
            else self.pictograph.blue_motion
        )
        dash_motion = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.motion_type == DASH
            else self.pictograph.blue_motion
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
        return self.pictograph.arrows[RED if self.a.color == BLUE else BLUE]

    def _default_zero_turns_dash_location(self) -> Locations:
        location_map = {
            (NORTH, SOUTH): EAST,
            (EAST, WEST): SOUTH,
            (SOUTH, NORTH): WEST,
            (WEST, EAST): NORTH,
        }
        return location_map.get((self.a.motion.start_loc, self.a.motion.end_loc))

    def get_static_location(self) -> Locations:
        return self.a.motion.start_loc
