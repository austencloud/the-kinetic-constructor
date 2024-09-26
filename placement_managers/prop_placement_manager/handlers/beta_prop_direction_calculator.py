from typing import TYPE_CHECKING
from data.constants import (
    BLUE,
    BOX,
    DIAMOND,
    DOWNLEFT,
    DOWNRIGHT,
    NONRADIAL,
    EAST,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    RADIAL,
    RED,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    UPLEFT,
    UPRIGHT,
    WEST,
    LEFT,
    RIGHT,
    UP,
    DOWN,
)

from objects.motion.motion import Motion
from objects.prop.prop import Prop

if TYPE_CHECKING:
    from placement_managers.prop_placement_manager.prop_placement_manager import (
        PropPlacementManager,
    )


class BetaPropDirectionCalculator:
    def __init__(self, placement_manager: "PropPlacementManager") -> None:
        self.main_widget = placement_manager.pictograph.main_widget

    def get_dir(self, motion: Motion) -> str:
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

    def get_direction_for_nonradial_I(self, motion: Motion) -> str:
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

    def get_direction_for_radial_I(self, motion: Motion) -> str:
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

    def get_dir_for_radial(self, motion: Motion) -> str:
        direction_map = {
            (NORTH, EAST): RIGHT,
            (NORTH, WEST): LEFT,
            (SOUTH, EAST): RIGHT,
            (SOUTH, WEST): LEFT,
            (EAST, NORTH): UP,
            (EAST, SOUTH): DOWN,
            (WEST, NORTH): UP,
            (WEST, SOUTH): DOWN,
            # Adding diagonal directions
            (NORTHEAST, SOUTHEAST): DOWNRIGHT,
            (NORTHEAST, NORTHWEST): UPLEFT,
            (SOUTHEAST, NORTHEAST): UPRIGHT,
            (SOUTHEAST, SOUTHWEST): DOWNLEFT,
            (SOUTHWEST, SOUTHEAST): UPLEFT,
            (SOUTHWEST, NORTHWEST): UPLEFT,
            (NORTHWEST, SOUTHWEST): DOWNLEFT,
            (NORTHWEST, NORTHEAST): UPRIGHT,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def get_dir_for_nonradial(self, motion: Motion) -> str:
        direction_map = {
            (NORTH, EAST): UP,
            (NORTH, WEST): DOWN,
            (SOUTH, EAST): UP,
            (SOUTH, WEST): DOWN,
            (EAST, NORTH): RIGHT,
            (EAST, SOUTH): LEFT,
            (WEST, NORTH): RIGHT,
            (WEST, SOUTH): LEFT,
            # Adding diagonal directions
            (NORTHEAST, SOUTHEAST): UPRIGHT,
            (NORTHEAST, NORTHWEST): UPRIGHT,
            (SOUTHEAST, NORTHEAST): DOWNRIGHT,
            (SOUTHEAST, SOUTHWEST): DOWNRIGHT,
            (SOUTHWEST, SOUTHEAST): UPLEFT,
            (SOUTHWEST, NORTHWEST): DOWNLEFT,
            (NORTHWEST, SOUTHWEST): UPLEFT,
            (NORTHWEST, NORTHEAST): DOWNLEFT,
        }
        return direction_map.get((motion.end_loc, motion.start_loc))

    def get_dir_for_non_shift(self, prop: Prop) -> str:
        diamond_layer_reposition_map = {
            RADIAL: {
                (NORTH, RED): RIGHT,
                (NORTH, BLUE): LEFT,
                (EAST, RED): DOWN,
                (EAST, BLUE): UP,
                (SOUTH, RED): LEFT,
                (SOUTH, BLUE): RIGHT,
                (WEST, BLUE): DOWN,
                (WEST, RED): UP,
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
        box_layer_reposition_map = {
            RADIAL: {
                (NORTHEAST, RED): DOWNRIGHT,
                (NORTHEAST, BLUE): UPLEFT,
                (SOUTHEAST, RED): UPRIGHT,
                (SOUTHEAST, BLUE): DOWNLEFT,
                (SOUTHWEST, RED): DOWNRIGHT,
                (SOUTHWEST, BLUE): UPLEFT,
                (NORTHWEST, RED): UPRIGHT,
                (NORTHWEST, BLUE): DOWNLEFT,
            },
            NONRADIAL: {
                (NORTHEAST, RED): UPRIGHT,
                (NORTHEAST, BLUE): DOWNLEFT,
                (SOUTHEAST, RED): DOWNRIGHT,
                (SOUTHEAST, BLUE): UPLEFT,
                (SOUTHWEST, RED): UPRIGHT,
                (SOUTHWEST, BLUE): DOWNLEFT,
                (NORTHWEST, RED): DOWNRIGHT,
                (NORTHWEST, BLUE): UPLEFT,
            },
        }
        if self.main_widget.grid_mode == DIAMOND:
            if prop.check.is_radial():
                return diamond_layer_reposition_map[RADIAL][(prop.loc, prop.color)]
            elif prop.check.is_nonradial():
                return diamond_layer_reposition_map[NONRADIAL][(prop.loc, prop.color)]
        elif self.main_widget.grid_mode == BOX:
            if prop.check.is_radial():
                return box_layer_reposition_map[RADIAL][(prop.loc, prop.color)]
            elif prop.check.is_nonradial():
                return box_layer_reposition_map[NONRADIAL][(prop.loc, prop.color)]

    def get_opposite_dir(self, movement: str) -> str:
        opposite_directions = {
            LEFT: RIGHT,
            RIGHT: LEFT,
            UP: DOWN,
            DOWN: UP,
            DOWNRIGHT: UPLEFT,
            UPLEFT: DOWNRIGHT,
            UPRIGHT: DOWNLEFT,
            DOWNLEFT: UPRIGHT,
        }
        return opposite_directions.get(movement)
