from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import Locations, MotionTypes
from constants import *

if TYPE_CHECKING:
    from objects.motion.motion import Motion


class ArrowLocationManager:
    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def _update_location(self) -> None:
        if not self.motion.arrow.is_ghost and self.motion.arrow.ghost:
            if not self.motion.arrow.loc:
                loc = self.get_arrow_location(
                    self.motion.start_loc, self.motion.end_loc, self.motion.motion_type
                )
                self.motion.arrow.loc = loc
                self.motion.arrow.ghost.loc = loc
                self.is_dragging = True

    def get_arrow_location(
        self, start_loc: str, end_loc: str, motion_type: MotionTypes
    ) -> Locations:
        if motion_type in [PRO, ANTI, FLOAT]:
            return self.get_shift_location(start_loc, end_loc)
        elif motion_type == DASH:
            return self.get_dash_location()
        elif motion_type == STATIC:
            return start_loc
        else:
            print("ERROR: Arrow motion type not found")
            return None

    def get_shift_location(self, start_loc: str, end_loc: str) -> str:
        # Simplified by using a single lookup that covers both directions
        direction_map = {
            frozenset({NORTH, EAST}): NORTHEAST,
            frozenset({EAST, SOUTH}): SOUTHEAST,
            frozenset({SOUTH, WEST}): SOUTHWEST,
            frozenset({WEST, NORTH}): NORTHWEST,
        }
        return direction_map.get(frozenset({start_loc, end_loc}))

    def get_dash_location(self) -> str:
        if self.motion.color == BLUE:
            other_color = RED
        else:  # self.motion.color is red
            other_color = BLUE

        other_motion_start_loc = self.motion.scene.pictograph_dict[f"{other_color}_start_loc"]
        other_motion_end_loc = self.motion.scene.pictograph_dict[f"{other_color}_end_loc"]
        other_motion_type = self.motion.scene.pictograph_dict[f"{other_color}_motion_type"]

        other_arrow_loc: Locations = None

        if other_motion_type in [PRO, ANTI, FLOAT]:
            vertical_map = {
                SOUTHEAST: WEST,
                NORTHEAST: WEST,
                SOUTHWEST: EAST,
                NORTHWEST: EAST,
            }
            horizontal_map = {
                SOUTHEAST: NORTH,
                SOUTHWEST: NORTH,
                NORTHEAST: SOUTH,
                NORTHWEST: SOUTH,
            }
            other_arrow_loc = self.get_arrow_location(
                other_motion_start_loc, other_motion_end_loc, other_motion_type
            )
            if self.motion.end_loc in [NORTH, SOUTH]:
                return vertical_map.get(other_arrow_loc)
            elif self.motion.end_loc in [EAST, WEST]:
                return horizontal_map.get(other_arrow_loc)

        elif (
            self.motion.motion_type == DASH and other_motion_type == DASH
        ):  # Type5 Letters
            if self.motion.turns == 0:
                direction_map = {
                    NORTH: SOUTH,
                    SOUTH: NORTH,
                    EAST: WEST,
                    WEST: EAST,
                }

                color_direction_map = {
                    BLUE: {
                        NORTH: WEST,
                        EAST: NORTH,
                        SOUTH: EAST,
                        WEST: SOUTH,
                    },
                    RED: {
                        NORTH: EAST,
                        EAST: SOUTH,
                        SOUTH: WEST,
                        WEST: NORTH,
                    },
                }

                if other_arrow_loc:
                    return direction_map.get(other_arrow_loc)
                else:
                    if not self.motion.arrow.loc:
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
                        self.motion.arrow.loc = loc_map.get(
                            (
                                (self.motion.start_loc, self.motion.end_loc),
                                other_motion_end_loc,
                            )
                        )
                        return color_direction_map.get(self.motion.color).get(
                            self.motion.arrow.loc
                        )
                    else:
                        return color_direction_map.get(self.motion.color).get(
                            self.motion.arrow.loc
                        )

            elif self.motion.turns > 0:
                if self.motion.prop_rot_dir == CLOCKWISE:
                    if self.motion.start_loc == NORTH and self.motion.end_loc == SOUTH:
                        return EAST
                    elif self.motion.start_loc == EAST and self.motion.end_loc == WEST:
                        return SOUTH
                    elif (
                        self.motion.start_loc == SOUTH and self.motion.end_loc == NORTH
                    ):
                        return WEST
                    elif self.motion.start_loc == WEST and self.motion.end_loc == EAST:
                        return NORTH
                elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    if self.motion.start_loc == NORTH and self.motion.end_loc == SOUTH:
                        return WEST
                    elif self.motion.start_loc == EAST and self.motion.end_loc == WEST:
                        return NORTH
                    elif (
                        self.motion.start_loc == SOUTH and self.motion.end_loc == NORTH
                    ):
                        return EAST
                    elif self.motion.start_loc == WEST and self.motion.end_loc == EAST:
                        return SOUTH

        elif other_motion_type == STATIC:
            other_arrow_loc = self.motion.scene.pictograph_dict[f"{other_color}_start_loc"]
            if self.motion.scene.pictograph_dict[LETTER] == "Λ":
                if other_arrow_loc == NORTH:
                    return SOUTH
                elif other_arrow_loc == SOUTH:
                    return NORTH
                elif other_arrow_loc == EAST:
                    return WEST
                elif other_arrow_loc == WEST:
                    return EAST
            elif self.motion.scene.pictograph_dict[LETTER] in ["Φ", "Ψ"]:
                if other_arrow_loc in [NORTH, SOUTH]:
                    if self.motion.color == BLUE:
                        return WEST
                    else:
                        return EAST
                elif other_arrow_loc in [EAST, WEST]:
                    if self.motion.color == BLUE:
                        return SOUTH
                    else:
                        return NORTH
