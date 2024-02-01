from typing import TYPE_CHECKING, Optional
from constants import *
from utilities.TypeChecking.TypeChecking import Locations, Orientations, PropRotDirs

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleCalculator:
    def __init__(self, arrow: "Arrow") -> None:
        self.arrow = arrow
        self.angle_resolvers = {
            PRO: self._get_pro_anti_angle,
            ANTI: self._get_pro_anti_angle,
            DASH: self._get_dash_angle,
            STATIC: self._get_static_angle,
        }

        if hasattr(self.arrow.scene, LETTER):
            self.other_motion = self.arrow.scene.get.other_motion(self.arrow.motion)

    def update_rotation(self) -> None:
        angle = self._resolve_angle()
        self._apply_rotation(angle)

    def _resolve_angle(self) -> int:
        rotation_override = self._get_final_rot_angle_override()
        if rotation_override == 0 or rotation_override:
            return rotation_override
        if hasattr(self.arrow.scene, LETTER):
            return self.angle_resolvers.get(self.arrow.motion.motion_type, lambda: 0)()
        return self.angle_resolvers.get(self.arrow.motion.motion_type, lambda: 0)()

    def _get_final_rot_angle_override(self) -> Optional[int]:
        special_manager = self.arrow.scene.arrow_placement_manager.special_positioner
        if special_manager:
            rotation_override = self.arrow.scene.wasd_manager.rotation_angle_override_manager.get_rot_angle_override_from_placements_dict(
                self.arrow
            )
            if rotation_override is True:
                return self._get_rot_angle_override_according_to_loc(rotation_override)
        return None

    def _get_rot_angle_override_according_to_loc(self, rotation_override: int) -> int:
        static_angle_override_map = {
            NORTH: 0,
            EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            SOUTH: 180,
            WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
        }
        dash_angle_override_map = {
            NORTH: 270,
            EAST: {CLOCKWISE: 0, COUNTER_CLOCKWISE: 180},
            SOUTH: 90,
            WEST: {CLOCKWISE: 180, COUNTER_CLOCKWISE: 0},
        }
        if self.arrow.motion.motion_type == DASH:
            if rotation_override == 0:
                loc_angle = dash_angle_override_map.get(self.arrow.loc)
                if isinstance(loc_angle, dict):
                    return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
                return loc_angle
        elif self.arrow.motion.motion_type == STATIC:
            if rotation_override == 0:
                loc_angle = static_angle_override_map.get(self.arrow.loc)
                if isinstance(loc_angle, dict):
                    return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
                return loc_angle

        return rotation_override

    def _apply_rotation(self, angle: int) -> None:
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)
        if self.arrow.ghost:
            self.arrow.ghost.setRotation(angle)

    def _get_pro_anti_angle(self) -> int:
        if self.arrow.motion.start_ori in [IN, OUT]:
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
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER] and self.arrow.turns in [
            0.5,
            1.5,
            2.5,
        ]:
            direction_map = {
                PRO: {
                    CLOCKWISE: {
                        NORTHEAST: 360,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 360,
                    },
                },
                ANTI: {
                    CLOCKWISE: {
                        NORTHEAST: 270,
                        SOUTHEAST: 180,
                        SOUTHWEST: 90,
                        NORTHWEST: 360,
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: 360,
                        SOUTHEAST: 90,
                        SOUTHWEST: 180,
                        NORTHWEST: 270,
                    },
                },
            }
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
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
        return direction_map[self.arrow.motion.motion_type][
            self.arrow.motion.prop_rot_dir
        ].get(self.arrow.loc, 0)

    def _get_motion_specific_angle(self) -> int:
        motion_type = self.arrow.motion.motion_type
        if motion_type in [PRO, ANTI]:
            return self._get_shift_angle()
        elif motion_type == STATIC:
            return self._get_static_angle()
        elif motion_type == DASH:
            return self._get_dash_angle()
        return 0

    def _get_static_angle(self) -> int:
        direction_map = self._get_static_direction_map()
        return direction_map.get(self.arrow.motion.prop_rot_dir, {}).get(
            self.arrow.loc, 0
        )

    def _get_static_direction_map(
        self,
    ) -> dict[Orientations, dict[PropRotDirs, dict[Locations, int]]]:
        orientation_map = {

            RADIAL: {
                CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },
            NONRADIAL: {
                CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
                COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
                NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
            },

        }
        if self.arrow.motion.start_ori in [IN, OUT]:
            return orientation_map.get(RADIAL)
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            return orientation_map.get(NONRADIAL)

    def _get_shift_angle(self) -> int:
        if self.arrow.motion.motion_type == PRO:
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
        elif self.arrow.motion.motion_type == ANTI:
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

    def _get_dash_angle(
        self,
    ) -> dict[Orientations, dict[PropRotDirs, dict[Locations, int]]]:
        if self.arrow.motion.prop_rot_dir == NO_ROT:
            orientation_map = {
                RADIAL: {
                    (NORTH, SOUTH): 0,
                    (EAST, WEST): 90,
                    (SOUTH, NORTH): 180,
                    (WEST, EAST): 270,
                },
                NONRADIAL: {
                    (NORTH, SOUTH): 90,
                    (EAST, WEST): 180,
                    (SOUTH, NORTH): 270,
                    (WEST, EAST): 0,
                },
            }

            if self.arrow.motion.start_ori in [IN, OUT]:
                return orientation_map.get(RADIAL).get(
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc)
                )
            elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
                return orientation_map.get(NONRADIAL).get(
                    (self.arrow.motion.start_loc, self.arrow.motion.end_loc)
                )
        elif self.arrow.motion.prop_rot_dir in [CLOCKWISE, COUNTER_CLOCKWISE]:
            orientation_map = {
                IN: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
                },
                OUT: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                },
                CLOCK: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
                    NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                },
                COUNTER: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
                    NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
                },
            }
            return (
                orientation_map.get(self.arrow.motion.start_ori)
                .get(self.arrow.motion.prop_rot_dir)
                .get(self.arrow.loc)
            )
