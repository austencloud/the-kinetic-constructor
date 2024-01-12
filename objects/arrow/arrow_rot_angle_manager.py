from typing import TYPE_CHECKING, Dict, Optional
from constants import *
from utilities.TypeChecking.TypeChecking import Locations, Orientations, PropRotDirs

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleManager:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.angle_resolvers = {
            PRO: self._get_pro_anti_angle,
            ANTI: self._get_pro_anti_angle,
            DASH: self._get_dash_angle,
            STATIC: self._get_static_angle,
        }
        self.letter_specific_resolvers = {
            "Y": self._get_Y_Z_angle,
            "Z": self._get_Y_Z_angle,
            "Φ": self._get_Φ_angle,
            "Ψ": self._get_Ψ_angle,
            "Λ": self._get_Λ_angle,
            "Φ-": self._get_Φ_dash_angle,
            "Ψ-": self._get_Ψ_dash_angle,
            "Λ-": self._get_Λ_dash_angle,
        }

    def update_rotation(self) -> None:
        angle = self._resolve_angle()
        self._apply_rotation(angle)

    def _resolve_angle(self) -> int:
        rotation_override = self._get_rotation_override()
        if rotation_override == 0 or rotation_override:
            return rotation_override
        if hasattr(self.arrow.scene, LETTER):
            letter_angle_resolver = self.letter_specific_resolvers.get(
                self.arrow.scene.letter
            )
            if letter_angle_resolver:
                return letter_angle_resolver()
            return self.angle_resolvers.get(self.arrow.motion.motion_type, lambda: 0)()
        return self.angle_resolvers.get(self.arrow.motion.motion_type, lambda: 0)()

    def _get_rotation_override(self) -> Optional[int]:
        special_manager = (
            self.arrow.scene.arrow_placement_manager.special_placement_manager
        )
        if special_manager:
            rotation_override = special_manager.get_rotation_angle_override(self.arrow)
            if rotation_override == 0 or rotation_override:
                return self._adjust_angle_according_to_location(rotation_override)
        return None

    def _adjust_angle_according_to_location(self, rotation_override: int) -> int:
        if rotation_override == 0:
            if self.arrow.loc == NORTH:
                return 0
            elif self.arrow.loc == EAST:
                if self.arrow.motion.prop_rot_dir == CLOCKWISE:
                    return 90
                elif self.arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    return 270
            elif self.arrow.loc == SOUTH:
                return 180
            elif self.arrow.loc == WEST:
                if self.arrow.motion.prop_rot_dir == CLOCKWISE:
                    return 270
                elif self.arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                    return 90
                

        return rotation_override

    def _apply_rotation(self, angle: int) -> None:
        self.arrow.set_arrow_transform_origin_to_center()
        self.arrow.setRotation(angle)
        if self.arrow.ghost:
            self.arrow.ghost.setRotation(angle)

    def _get_pro_anti_angle(self) -> int:
        direction_map = {
            PRO: {
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
            },
            ANTI: {
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
            },
        }
        return direction_map[self.arrow.motion_type][
            self.arrow.motion.prop_rot_dir
        ].get(self.arrow.loc, 0)

    def _get_dash_angle(self) -> int:
        return self._get_default_dash_angle()

    def _get_static_angle(self) -> int:
        direction_map = {
            IN: {
                CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
                COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },
            OUT: {
                CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },
        }
        return (
            direction_map.get(self.arrow.motion.start_ori)
            .get(self.arrow.motion.prop_rot_dir)
            .get(self.arrow.loc)
        )

    def _get_rot_angle(self) -> int:
        letter_specific_angle = self._get_letter_specific_angle()
        if letter_specific_angle is not None:
            return letter_specific_angle

        return self._get_motion_specific_angle()

    def _get_letter_specific_angle(self) -> int:
        letter = getattr(self.arrow.scene, LETTER, None)
        angle_method_mapping = {
            "Y": self._get_Y_Z_angle,
            "Z": self._get_Y_Z_angle,
            "Φ": self._get_Φ_angle,
            "Ψ": self._get_Ψ_angle,
            "Λ": self._get_Λ_angle,
            "Φ-": self._get_Φ_dash_angle,
            "Ψ-": self._get_Ψ_dash_angle,
            "Λ-": self._get_Λ_dash_angle,
        }
        return angle_method_mapping.get(letter, lambda: None)()

    def _get_motion_specific_angle(self) -> int:
        motion_type = self.arrow.motion_type
        if motion_type in [PRO, ANTI]:
            return self._get_default_shift_angle()
        elif motion_type == STATIC:
            return self._get_default_static_angle()
        elif motion_type == DASH:
            return self._get_default_dash_angle()
        return 0

    def _get_default_static_angle(self) -> int:
        direction_map = self._get_static_direction_map()
        return direction_map.get(self.arrow.motion.prop_rot_dir, {}).get(
            self.arrow.loc, 0
        )

    def _get_static_direction_map(
        self,
    ) -> Dict[Orientations, Dict[PropRotDirs, Dict[Locations, int]]]:
        orientation_map = {
            IN: {
                CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
                COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },
            OUT: {
                CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },
        }
        return orientation_map.get(self.arrow.motion.start_ori, {})

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
                    .get(self.arrow.loc, 0)
                )
            elif self.arrow.motion.start_ori == OUT:
                return (
                    {
                        CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                        COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                        NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                    }
                    .get(self.arrow.motion.prop_rot_dir, {})
                    .get(self.arrow.loc, 0)
                )
        elif self.arrow.motion_type in [PRO, ANTI]:
            return self._get_default_shift_angle()
        return 0

    def _get_Λ_dash_angle(self) -> int:
        other_motion = (
            self.arrow.scene.motions[RED]
            if self.arrow.color == BLUE
            else self.arrow.scene.motions[BLUE]
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
        ).get(self.arrow.loc)
        return arrow_angle if self.arrow.loc else 0

    def _get_Φ_dash_angle(self) -> int:
        other_motion = (
            self.arrow.scene.motions[RED]
            if self.arrow.color == BLUE
            else self.arrow.scene.motions[BLUE]
        )
        if other_motion.arrow.loc:
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
            self.arrow.loc = arrow_loc
            self.arrow.ghost.loc = arrow_loc
            map = {
                (NORTH, SOUTH): {EAST: 90, WEST: 90},
                (SOUTH, NORTH): {EAST: 270, WEST: 270},
                (EAST, WEST): {NORTH: 180, SOUTH: 180},
                (WEST, EAST): {NORTH: 0, SOUTH: 0},
            }
            return map.get(
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc), {}
            ).get(self.arrow.loc)
        else:
            return self._get_default_dash_angle()

    def _get_Ψ_dash_angle(self) -> int:
        other_motion = (
            self.arrow.scene.motions[RED]
            if self.arrow.color == BLUE
            else self.arrow.scene.motions[BLUE]
        )
        if other_motion.arrow.loc:
            loc_map = {
                ((NORTH, SOUTH), (NORTH, SOUTH)): {RED: EAST, BLUE: WEST},
                ((SOUTH, NORTH), (SOUTH, NORTH)): {RED: EAST, BLUE: WEST},
                ((EAST, WEST), (EAST, WEST)): {RED: NORTH, BLUE: SOUTH},
                ((WEST, EAST), (WEST, EAST)): {RED: NORTH, BLUE: SOUTH},
            }
            arrow_loc = loc_map.get(
                (
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc),
                    (other_motion.start_loc, other_motion.end_loc),
                )
            ).get(self.arrow.color)
            self.arrow.loc = arrow_loc
            self.arrow.ghost.loc = arrow_loc
            map = {
                (NORTH, SOUTH): {EAST: 90, WEST: 90},
                (SOUTH, NORTH): {EAST: 270, WEST: 270},
                (EAST, WEST): {NORTH: 180, SOUTH: 180},
                (WEST, EAST): {NORTH: 0, SOUTH: 0},
            }
            return map.get(
                (self.arrow.motion.start_loc, self.arrow.motion.end_loc), {}
            ).get(self.arrow.loc)
        else:
            return self._get_default_dash_angle()

    def _get_Φ_angle(self) -> int:
        if self.arrow.turns == 0:
            if self.arrow.motion_type == DASH:
                return self._get_default_dash_angle()
            elif self.arrow.motion_type == STATIC:
                return self._get_default_static_angle()

    def _get_Ψ_angle(self) -> int:
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
            self.arrow.loc = loc_map.get(
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
