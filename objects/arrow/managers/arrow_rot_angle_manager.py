from typing import TYPE_CHECKING, Dict, Optional
from constants import *
from utilities.TypeChecking.TypeChecking import Locations, Orientations, PropRotDirs

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowRotAngleCalculator:
    def __init__(self, arrow: "Arrow") -> None:
        self.a = arrow
        self.angle_resolvers = {
            PRO: self._get_pro_anti_angle,
            ANTI: self._get_pro_anti_angle,
            DASH: self._get_dash_angle,
            STATIC: self._get_static_angle,
        }

        if hasattr(self.a.scene, LETTER):
            self.other_motion = self.a.scene.get.other_motion(self.a.motion)

    def update_rotation(self) -> None:
        angle = self._resolve_angle()
        self._apply_rotation(angle)

    def _resolve_angle(self) -> int:
        rotation_override = self._get_final_rot_angle_override()
        if rotation_override == 0 or rotation_override:
            return rotation_override
        if hasattr(self.a.scene, LETTER):
            return self.angle_resolvers.get(self.a.motion.motion_type, lambda: 0)()
        return self.angle_resolvers.get(self.a.motion.motion_type, lambda: 0)()

    def _get_final_rot_angle_override(self) -> Optional[int]:
        special_manager = self.a.scene.arrow_placement_manager.special_positioner
        if special_manager:
            rotation_override = self.a.scene.wasd_manager.rotation_manager.get_rot_angle_override_from_placements_dict(
                self.a
            )
            if rotation_override == 0 or rotation_override:
                return self._get_rot_angle_override_according_to_loc(rotation_override)
        return None

    def _get_rot_angle_override_according_to_loc(self, rotation_override: int) -> int:
        angle_map = {
            NORTH: 0,
            EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            SOUTH: 180,
            WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
        }

        if rotation_override == 0:
            loc_angle = angle_map.get(self.a.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.a.motion.prop_rot_dir, 0)
            return loc_angle

        return rotation_override

    def _apply_rotation(self, angle: int) -> None:
        self.a.setTransformOriginPoint(self.a.boundingRect().center())
        self.a.setRotation(angle)
        if self.a.ghost:
            self.a.ghost.setRotation(angle)

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
        return direction_map[self.a.motion_type][self.a.motion.prop_rot_dir].get(
            self.a.loc, 0
        )

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
            direction_map.get(self.a.motion.start_ori)
            .get(self.a.motion.prop_rot_dir)
            .get(self.a.loc)
        )

    def _get_motion_specific_angle(self) -> int:
        motion_type = self.a.motion_type
        if motion_type in [PRO, ANTI]:
            return self._get_shift_angle()
        elif motion_type == STATIC:
            return self._get_static_angle()
        elif motion_type == DASH:
            return self._get_dash_angle()
        return 0

    def _get_static_angle(self) -> int:
        direction_map = self._get_static_direction_map()
        return direction_map.get(self.a.motion.prop_rot_dir, {}).get(self.a.loc, 0)

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
        return orientation_map.get(self.a.motion.start_ori, {})

    def _get_shift_angle(self) -> int:
        if self.a.motion_type == PRO:
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
                .get(self.a.motion.prop_rot_dir)
                .get(self.a.loc)
            )
        elif self.a.motion_type == ANTI:
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
                .get(self.a.motion.prop_rot_dir, {})
                .get(self.a.loc, 0)
            )
        return 0

    def _get_dash_angle(
        self,
    ) -> Dict[Orientations, Dict[PropRotDirs, Dict[Locations, int]]]:
        if self.a.motion.prop_rot_dir == NO_ROT:
            return {
                (NORTH, SOUTH): 90,
                (SOUTH, NORTH): 270,
                (EAST, WEST): 180,
                (WEST, EAST): 0,
            }.get((self.a.motion.start_loc, self.a.motion.end_loc), {})

        elif self.a.motion.prop_rot_dir in [CLOCKWISE, COUNTER_CLOCKWISE]:
            orientation_map = {
                IN: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
                },
                OUT: {
                    CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                    COUNTER_CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                },
            }
            return (
                orientation_map.get(self.a.motion.start_ori)
                .get(self.a.motion.prop_rot_dir)
                .get(self.a.loc)
            )
