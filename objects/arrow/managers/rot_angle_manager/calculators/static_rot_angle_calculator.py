from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class StaticRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self) -> int:
        rotation_override = self.has_rotation_angle_override()
        if rotation_override:
            return self._get_rot_angle_override_according_to_loc()
        if self.arrow.motion.start_ori in [IN, OUT]:
            direction_map = self._radial_static_direction_map()
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            direction_map = self._nonradial_static_direction_map()

        prop_rot_dir = self.arrow.motion.prop_rot_dir
        loc = self.arrow.loc

        return direction_map.get(prop_rot_dir).get(loc, 0)

    def _radial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {
                NORTH: 0,
                EAST: 90,
                SOUTH: 180,
                WEST: 270,
                NORTHEAST: 45,
                SOUTHEAST: 135,
                SOUTHWEST: 225,
                NORTHWEST: 315,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 0,
                EAST: 270,
                SOUTH: 180,
                WEST: 90,
                NORTHEAST: 315,
                SOUTHEAST: 225,
                SOUTHWEST: 135,
                NORTHWEST: 45,
            },
            NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
        }

    def _nonradial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {
                NORTH: 180,
                EAST: 270,
                SOUTH: 0,
                WEST: 90,
                NORTHEAST: 135,
                SOUTHEAST: 225,
                SOUTHWEST: 315,
            },
            COUNTER_CLOCKWISE: {
                NORTH: 180,
                EAST: 90,
                SOUTH: 0,
                WEST: 270,
                NORTHEAST: 45,
                SOUTHEAST: 315,
                SOUTHWEST: 225,
            },
            NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
        }

    def _get_rot_angle_override_according_to_loc(self) -> int:
        static_from_radial_angle_override_map = {
            NORTH: 180,
            EAST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            SOUTH: 0,
            WEST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            NORTHEAST: 225,
            SOUTHEAST: 315,
            SOUTHWEST: 45,
            NORTHWEST: 135,
        }
        static_from_nonradial_angle_override_map = {
            NORTH: 0,
            EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            SOUTH: 180,
            WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            NORTHEAST: 45,
            SOUTHEAST: 315,
            SOUTHWEST: 225,
            NORTHWEST: 135,
        }
        if self.arrow.motion.start_ori in [IN, OUT]:
            loc_angle = static_from_radial_angle_override_map.get(self.arrow.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
            return loc_angle
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            loc_angle = static_from_nonradial_angle_override_map.get(self.arrow.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
            return loc_angle
