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

    def determine_direction_for_unilateral_props(
        self, red_motion: Motion
    ) -> Tuple[Directions]:
        """Determine the translation direction for big unilateral props based on the motion type, start location, end location."""
        red_direction = self.get_direction_for_motion(red_motion)
        blue_direction = self.get_opposite_direction(red_direction)
        return (red_direction or None, blue_direction or None)

    def get_direction_for_motion(self, motion: Motion) -> Directions:
        """Determine the direction based on a single motion."""
        if motion.end_ori in [
            IN,
            OUT,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_loc in [NORTH, SOUTH]:
                return RIGHT if motion.start_loc == EAST else LEFT
            elif motion.end_loc in [EAST, WEST]:
                return DOWN if motion.start_loc == SOUTH else UP
        elif motion.end_ori in [
            CLOCK,
            COUNTER,
        ] and motion.motion_type in [
            PRO,
            ANTI,
            STATIC,
        ]:
            if motion.end_loc in [NORTH, SOUTH]:
                return UP if motion.start_loc == EAST else DOWN
            elif motion.end_loc in [EAST, WEST]:
                return RIGHT if motion.start_loc == SOUTH else LEFT
        return None

    def determine_translation_dir(self, motion: Motion) -> Directions:
        """Determine the translation direction based on the motion type, start location, end location, and end layer."""
        if not (motion.is_shift() or motion.is_static()):
            return None

        if motion.prop.is_radial():
            return self._get_translation_dir_for_radial(motion)
        elif motion.prop.is_antiradial():
            return self._get_translation_dir_for_antiradial(motion)

    def _get_translation_dir_for_radial(self, motion: Motion) -> Directions:
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

    def _get_translation_dir_for_antiradial(self, motion: Motion) -> Directions:
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

    def _get_dir_for_non_shift(self, prop: Prop) -> Directions:
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
        if prop.is_radial():
            return layer_reposition_map[RADIAL][(prop.loc, prop.color)]
        elif prop.is_antiradial():
            return layer_reposition_map[ANTIRADIAL][(prop.loc, prop.color)]

    def get_opposite_direction(self, movement: Directions) -> Directions:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
        }
        return opposite_directions.get(movement)
