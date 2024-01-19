from typing import TYPE_CHECKING, Tuple
from constants import (
    ANTIRADIAL,
    BLUE,
    CLOCK,
    COUNTER,
    EAST,
    IN,
    NORTH,
    OUT,
    RADIAL,
    RED,
    SOUTH,
    WEST,
    PRO,
    ANTI,
    STATIC,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)

from objects.motion.motion import Motion
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Directions

if TYPE_CHECKING:
    pass


class BetaPropDirectionCalculator:
    def __init__(self, prop_placement_manager) -> None:
        self.prop_placement_manager = prop_placement_manager

    def get_dir(self, motion: Motion) -> Directions:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if not (motion.is_shift() or motion.is_static()):
            return None

        if motion.prop.check.is_radial():
            return self.get_dir_for_radial(motion)
        elif motion.prop.check.is_antiradial():
            return self.get_dir_for_antiradial(motion)

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

    def get_dir_for_antiradial(self, motion: Motion) -> Directions:
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
                (SOUTH, RED): RIGHT,
                (SOUTH, BLUE): LEFT,
                (EAST, RED): UP,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
                (EAST, BLUE): DOWN,
            },
            ANTIRADIAL: {
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
        elif prop.check.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.loc, prop.color)]

    def get_opposite_dir(self, movement: Directions) -> Directions:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
        }
        return opposite_directions.get(movement)
