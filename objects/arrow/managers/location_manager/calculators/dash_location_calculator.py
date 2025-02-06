from Enums.Enums import Letter
from Enums.letters import LetterType
from data.constants import *
from objects.motion.motion import Motion
from .base_location_calculator import BaseLocationCalculator
from typing import TYPE_CHECKING




class DashLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        if self.pictograph.letter in [Letter.Φ_DASH, Letter.Ψ_DASH]:
            return self._get_Φ_dash_Ψ_dash_location()
        elif (
            self.pictograph.letter in [Letter.Λ, Letter.Λ_DASH]
            and self.arrow.motion.turns == 0
        ):
            return self._get_Λ_zero_turns_location()
        elif self.arrow.motion.turns == 0:
            return self._default_zero_turns_dash_location()
        else:
            return self._dash_location_non_zero_turns()

    def _get_Φ_dash_Ψ_dash_location(self) -> str:
        self.other_motion = self.pictograph.get.other_motion(self.arrow.motion)

        if self.arrow.motion.turns == 0 and self.other_motion.arrow.motion.turns == 0:
            location_map = {
                (RED, (NORTH, SOUTH)): EAST,
                (RED, (EAST, WEST)): NORTH,
                (RED, (SOUTH, NORTH)): EAST,
                (RED, (WEST, EAST)): NORTH,
                (BLUE, (NORTH, SOUTH)): WEST,
                (BLUE, (EAST, WEST)): SOUTH,
                (BLUE, (SOUTH, NORTH)): WEST,
                (BLUE, (WEST, EAST)): SOUTH,
                (RED, (NORTHWEST, SOUTHEAST)): NORTHEAST,
                (RED, (NORTHEAST, SOUTHWEST)): SOUTHEAST,
                (RED, (SOUTHWEST, NORTHEAST)): SOUTHEAST,
                (RED, (SOUTHEAST, NORTHWEST)): NORTHEAST,
                (BLUE, (NORTHWEST, SOUTHEAST)): SOUTHWEST,
                (BLUE, (NORTHEAST, SOUTHWEST)): NORTHWEST,
                (BLUE, (SOUTHWEST, NORTHEAST)): NORTHWEST,
                (BLUE, (SOUTHEAST, NORTHWEST)): SOUTHWEST,
            }
            arrow_location = location_map.get(
                (
                    self.arrow.color,
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                )
            )
            return arrow_location

        elif self.arrow.motion.turns == 0:
            return self.pictograph.get.opposite_location(
                self._dash_location_non_zero_turns(self.other_motion)
            )
        elif self.arrow.motion.turns != 0:
            return self._dash_location_non_zero_turns(self.arrow.motion)

    def _get_Λ_zero_turns_location(self) -> str:
        self.other_motion = self.pictograph.get.other_motion(self.arrow.motion)
        loc_map = {
            ((NORTH, SOUTH), WEST): EAST,
            ((EAST, WEST), SOUTH): NORTH,
            ((NORTH, SOUTH), EAST): WEST,
            ((WEST, EAST), SOUTH): NORTH,
            ((SOUTH, NORTH), WEST): EAST,
            ((EAST, WEST), NORTH): SOUTH,
            ((SOUTH, NORTH), EAST): WEST,
            ((WEST, EAST), NORTH): SOUTH,
            ((NORTHEAST, SOUTHWEST), NORTHWEST): SOUTHEAST,
            ((NORTHWEST, SOUTHEAST), NORTHEAST): SOUTHWEST,
            ((SOUTHWEST, NORTHEAST), SOUTHEAST): NORTHWEST,
            ((SOUTHEAST, NORTHWEST), SOUTHWEST): NORTHEAST,
            ((NORTHEAST, SOUTHWEST), SOUTHEAST): NORTHWEST,
            ((NORTHWEST, SOUTHEAST), SOUTHWEST): NORTHEAST,
            ((SOUTHWEST, NORTHEAST), NORTHWEST): SOUTHEAST,
            ((SOUTHEAST, NORTHWEST), NORTHEAST): SOUTHWEST,
        }
        arrow_location = loc_map.get(
            (
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                (self.other_motion.end_loc),
            )
        )
        return arrow_location

    def _default_zero_turns_dash_location(self) -> str:
        if self.pictograph.letter_type == LetterType.Type3:
            return self._calculate_dash_location_based_on_shift()

        location_map = {
            (NORTH, SOUTH): EAST,
            (EAST, WEST): SOUTH,
            (SOUTH, NORTH): WEST,
            (WEST, EAST): NORTH,
            (NORTHEAST, SOUTHWEST): SOUTHEAST,
            (NORTHWEST, SOUTHEAST): NORTHEAST,
            (SOUTHWEST, NORTHEAST): NORTHWEST,
            (SOUTHEAST, NORTHWEST): SOUTHWEST,
        }
        return location_map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc), ""
        )

    def _dash_location_non_zero_turns(self, motion: Motion = None) -> str:
        motion = motion if motion else self.arrow.motion
        loc_map = {
            CLOCKWISE: {
                NORTH: EAST,
                EAST: SOUTH,
                SOUTH: WEST,
                WEST: NORTH,
                NORTHEAST: SOUTHEAST,
                SOUTHEAST: SOUTHWEST,
                SOUTHWEST: NORTHWEST,
                NORTHWEST: NORTHEAST,
            },
            COUNTER_CLOCKWISE: {
                NORTH: WEST,
                EAST: NORTH,
                SOUTH: EAST,
                WEST: SOUTH,
                NORTHEAST: NORTHWEST,
                SOUTHEAST: NORTHEAST,
                SOUTHWEST: SOUTHEAST,
                NORTHWEST: SOUTHWEST,
            },
        }
        return loc_map[motion.prop_rot_dir][motion.start_loc]

    def _calculate_dash_location_based_on_shift(self) -> str:
        shift_arrow = self.pictograph.get.shift().arrow

        shift_location = shift_arrow.loc
        diamond_dash_location_map = {
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
        box_dash_location_map = {
            (NORTHEAST, NORTH): SOUTHEAST,
            (NORTHEAST, EAST): NORTHWEST,
            (NORTHEAST, SOUTH): NORTHWEST,
            (NORTHEAST, WEST): SOUTHEAST,
            (SOUTHEAST, NORTH): SOUTHWEST,
            (SOUTHEAST, EAST): SOUTHWEST,
            (SOUTHEAST, SOUTH): NORTHEAST,
            (SOUTHEAST, WEST): NORTHEAST,
            (SOUTHWEST, NORTH): SOUTHEAST,
            (SOUTHWEST, EAST): NORTHWEST,
            (SOUTHWEST, SOUTH): NORTHWEST,
            (SOUTHWEST, WEST): SOUTHEAST,
            (NORTHWEST, NORTH): SOUTHWEST,
            (NORTHWEST, EAST): SOUTHWEST,
            (NORTHWEST, SOUTH): NORTHEAST,
            (NORTHWEST, WEST): NORTHEAST,
        }
        grid_mode = self.pictograph.grid_mode
        start_loc = self.arrow.motion.start_loc

        if grid_mode == DIAMOND:
            return diamond_dash_location_map.get((start_loc, shift_location))
        elif grid_mode == BOX:
            return box_dash_location_map.get((start_loc, shift_location))
