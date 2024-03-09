from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import (
    BLUE,
    NONRADIAL,
    EAST,
    NORTH,
    RADIAL,
    RED,
    SOUTH,
    WEST,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)

from objects.motion.motion import Motion
from objects.prop.prop import Prop
from Enums.Enums import Directions

if TYPE_CHECKING:
    pass


class BetaPropDirectionCalculator:
    def get_dir(self, motion: Motion) -> Directions:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if (
            motion.pictograph.letter == "I"
            and motion.pictograph.check.ends_with_radial_ori()
        ):
            return self.get_direction_for_radial_I(motion)
        elif (
            motion.pictograph.letter == "I"
            and motion.pictograph.check.ends_with_nonradial_ori()
        ):
            return self.get_direction_for_nonradial_I(motion)
        if motion.check.is_shift():
            if motion.prop.check.is_radial():
                return self.get_dir_for_radial(motion)
            elif motion.prop.check.is_nonradial():
                return self.get_dir_for_nonradial(motion)
        elif motion.check.is_dash() or motion.check.is_static():
            return self.get_dir_for_non_shift(motion.prop)

    def get_direction_for_nonradial_I(self, motion: Motion) -> Directions:
        direction_map = {
            (NORTH, RED): UP,
            (NORTH, BLUE): DOWN,
            (EAST, RED): RIGHT,
            (EAST, BLUE): LEFT,
            (SOUTH, RED): DOWN,
            (SOUTH, BLUE): UP,
            (WEST, BLUE): LEFT,
            (WEST, RED): RIGHT,
        }
        return direction_map.get((motion.end_loc, motion.prop.color))

    def get_direction_for_radial_I(self, motion: Motion) -> Directions:
        direction_map = {
            (NORTH, RED): RIGHT,
            (NORTH, BLUE): LEFT,
            (EAST, RED): DOWN,
            (EAST, BLUE): UP,
            (SOUTH, RED): LEFT,
            (SOUTH, BLUE): RIGHT,
            (WEST, BLUE): UP,
            (WEST, RED): DOWN,
        }
        return direction_map.get((motion.end_loc, motion.prop.color))

    def get_dir_for_radial(self, motion: Motion) -> Directions:
        direction_map = {
            (NORTH, EAST): RIGHT,
            (NORTH, WEST): LEFT,
            (SOUTH, EAST): RIGHT,
            (SOUTH, WEST): LEFT,
            (EAST, NORTH): UP,
            (EAST, SOUTH): DOWN,
            (WEST, NORTH): UP,
            (WEST, SOUTH): DOWN,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def get_dir_for_nonradial(self, motion: Motion) -> Directions:
        direction_map = {
            (NORTH, EAST): UP,
            (NORTH, WEST): DOWN,
            (SOUTH, EAST): UP,
            (SOUTH, WEST): DOWN,
            (EAST, NORTH): RIGHT,
            (EAST, SOUTH): LEFT,
            (WEST, NORTH): RIGHT,
            (WEST, SOUTH): LEFT,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def get_dir_for_non_shift(self, prop: Prop) -> Directions:
        layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (SOUTH, RED): LEFT,
                (SOUTH, BLUE): RIGHT,
                (EAST, RED): DOWN,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
                (EAST, BLUE): UP,
            },
            NONRADIAL: {
                (NORTH, RED): UP,
                (NORTH, BLUE): DOWN,
                (SOUTH, RED): UP,
                (SOUTH, BLUE): DOWN,
                (EAST, RED): RIGHT,
                (WEST, BLUE): LEFT,
                (WEST, RED): RIGHT,
                (EAST, BLUE): LEFT,
            },
        }
        if prop.check.is_radial():
            return layer_reposition_map[RADIAL][(prop.loc, prop.color)]
        elif prop.check.is_nonradial():
            return layer_reposition_map[NONRADIAL][(prop.loc, prop.color)]

    def get_opposite_dir(self, movement: Directions) -> Directions:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
        }
        return opposite_directions.get(movement)
