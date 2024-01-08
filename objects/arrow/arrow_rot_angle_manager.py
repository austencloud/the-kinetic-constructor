from typing import TYPE_CHECKING
from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleManager:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def update_rotation(self) -> None:
        angle = self._get_rot_angle()

        self.arrow.set_arrow_transform_origin_to_center()
        self.arrow.setRotation(angle)
        if not self.arrow.is_ghost:
            self.arrow.ghost.setRotation(angle)

    def _get_rot_angle(self) -> int:
        if hasattr(self.arrow.scene, "letter"):
            if self.arrow.scene.letter in ["Y", "Z"]:
                return self._get_Y_Z_angle()
            elif self.arrow.scene.letter == "Λ-":
                return self._get_Λ_dash_angle()
            elif self.arrow.scene.letter in ["Φ-", "Ψ-"]:
                return self._get_Φ_dash_Ψ_dash_angle()
            elif self.arrow.scene.letter in ["Φ", "Ψ"]:
                return self._get_Φ_Ψ_angle()
            elif self.arrow.scene.letter == "Λ":
                return self._get_Λ_angle()

        if self.arrow.motion_type in [PRO, ANTI]:
            return self._get_default_shift_angle()
        elif self.arrow.motion_type == STATIC:
            return self._get_default_static_angle()
        elif self.arrow.motion_type == DASH:
            return self._get_default_dash_angle()
        else:
            return 0

    def _get_default_static_angle(self) -> int:
        if self.arrow.motion.start_ori == IN:
            return (
                {
                    CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
                    COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
                    NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                }
                .get(self.arrow.motion.prop_rot_dir)
                .get(self.arrow.loc)
            )
        elif self.arrow.motion.start_ori == OUT:
            return (
                {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                }
                .get(self.arrow.motion.prop_rot_dir)
                .get(self.arrow.loc)
            )

        return 0

    def _get_default_shift_angle(self) -> int:
        if self.arrow.motion_type == PRO:
            return (
                {
                    CLOCKWISE: {
                        NORTHEAST: 0,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 0,
                    },
                }
                .get(self.arrow.motion.prop_rot_dir)
                .get(self.arrow.loc)
            )
        elif self.arrow.motion_type == ANTI:
            return (
                {
                    CLOCKWISE: {
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 0,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 0,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                }
                .get(self.arrow.motion.prop_rot_dir, {})
                .get(self.arrow.loc, 0)
            )
        return 0

    def _get_default_dash_angle(self) -> int:
        dash_loc_map = {
            (NORTH, SOUTH): {RED: EAST, BLUE: WEST},
            (SOUTH, NORTH): {RED: EAST, BLUE: WEST},
            (EAST, WEST): {RED: NORTH, BLUE: SOUTH},
            (WEST, EAST): {RED: NORTH, BLUE: SOUTH},
        }
        self.arrow.loc = dash_loc_map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc)
        ).get(self.arrow.color)
        dash_rot_map = {
            (NORTH, SOUTH): 90,
            (SOUTH, NORTH): 270,
            (EAST, WEST): 180,
            (WEST, EAST): 0,
        }
        return dash_rot_map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc)
        )

    def _get_Y_Z_angle(self) -> int:
        if self.arrow.motion_type == STATIC:
            if self.arrow.motion.start_ori == IN:
                return (
                    {
                        CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
                        COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
                        NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                    }
                    .get(self.arrow.motion.prop_rot_dir, {})
                    .get(self.loc, 0)
                )
            elif self.arrow.motion.start_ori == OUT:
                return (
                    {
                        CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                        COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                        NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                    }
                    .get(self.arrow.motion.prop_rot_dir, {})
                    .get(self.loc, 0)
                )
        elif self.arrow.motion_type in [PRO, ANTI]:
            return self._get_default_shift_angle()
        return 0

    def _get_Λ_dash_angle(self) -> int:
        other_motion = (
            self.arrow.scene.motions[RED] if self.arrow.color == BLUE else self.arrow.scene.motions[BLUE]
        )
        loc_map = {
            ((NORTH, SOUTH), (EAST, WEST)): {EAST: 90},
            ((EAST, WEST), (NORTH, SOUTH)): {NORTH: 180},
            ((NORTH, SOUTH), (WEST, EAST)): {WEST: 90},
            ((WEST, EAST), (NORTH, SOUTH)): {NORTH: 0},
            ((SOUTH, NORTH), (EAST, WEST)): {EAST: 270},
            ((EAST, WEST), (SOUTH, NORTH)): {SOUTH: 180},
            ((SOUTH, NORTH), (WEST, EAST)): {WEST: 270},
            ((WEST, EAST), (SOUTH, NORTH)): {SOUTH: 0},
        }
        arrow_angle = loc_map.get(
            (
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                (other_motion.start_loc, other_motion.end_loc),
            )
        ).get(self.loc)
        return arrow_angle if self.loc else 0

    def _get_Φ_dash_Ψ_dash_angle(self) -> int:
        other_motion = (
            self.arrow.scene.motions[RED] if self.arrow.color == BLUE else self.arrow.scene.motions[BLUE]
        )
        loc_map = {
            ((NORTH, SOUTH), (SOUTH, NORTH)): {RED: EAST, BLUE: WEST},
            ((SOUTH, NORTH), (NORTH, SOUTH)): {RED: EAST, BLUE: WEST},
            ((EAST, WEST), (WEST, EAST)): {RED: NORTH, BLUE: SOUTH},
            ((WEST, EAST), (EAST, WEST)): {RED: NORTH, BLUE: SOUTH},
        }
        arrow_loc = loc_map.get(
            (
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                (other_motion.start_loc, other_motion.end_loc),
            )
        ).get(self.arrow.color)
        self.loc = arrow_loc
        self.arrow.ghost.loc = arrow_loc
        map = {
            (NORTH, SOUTH): {EAST: 90, WEST: 90},
            (SOUTH, NORTH): {EAST: 270, WEST: 270},
            (EAST, WEST): {NORTH: 180, SOUTH: 180},
            (WEST, EAST): {NORTH: 0, SOUTH: 0},
        }
        return map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc), {}
        ).get(self.loc)

    def _get_Φ_Ψ_angle(self) -> int:
        if self.arrow.turns == 0:
            if self.arrow.motion_type == DASH:
                return self._get_default_dash_angle()
            elif self.arrow.motion_type == STATIC:
                return self._get_default_static_angle()

    def _get_Λ_angle(self) -> int:
        if self.arrow.motion_type == DASH:
            other_motion = (
                self.arrow.scene.motions[RED]
                if self.arrow.color == BLUE
                else self.arrow.scene.motions[BLUE]
            )
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
            self.loc = loc_map.get(
                (
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                    other_motion.end_loc,
                )
            )

            rot_map = {
                (NORTH, SOUTH): 90,
                (SOUTH, NORTH): 270,
                (EAST, WEST): 180,
                (WEST, EAST): 0,
            }
            return rot_map.get((self.arrow.motion.start_loc, self.arrow.motion.end_loc))
        elif self.arrow.motion_type == STATIC:
            return self._get_default_static_angle()
