from constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class StaticRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self) -> int:
        rotation_override = self.has_rotation_angle_override()
        if rotation_override:
            return self._get_rot_angle_override_according_to_loc()
        if self.arrow.motion.start_ori in [IN, OUT]:
            direction_map = self._radial_static_direction_map()
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            direction_map = self._non_radial_static_direction_map()

        prop_rot_dir = self.arrow.motion.prop_rot_dir
        loc = self.arrow.loc

        return direction_map.get(prop_rot_dir).get(loc, 0)

    def _radial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
            COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
            NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
        }

    def _non_radial_static_direction_map(self) -> dict[str, dict[str, int]]:
        return {
            CLOCKWISE: {NORTH: 180, EAST: 270, SOUTH: 0, WEST: 90},
            COUNTER_CLOCKWISE: {NORTH: 180, EAST: 90, SOUTH: 0, WEST: 270},
            NO_ROT: {NORTH: 0, SOUTH: 0, EAST: 0, WEST: 0},
        }

    def _get_rot_angle_override_according_to_loc(self) -> int:

        static_from_layer1_angle_override_map = {
            NORTH: 180,
            EAST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            SOUTH: 0,
            WEST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
        }
        static_from_layer2_angle_override_map = {
            NORTH: 0,
            EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            SOUTH: 180,
            WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
        }
        if self.arrow.motion.start_ori in [IN, OUT]:
            loc_angle = static_from_layer1_angle_override_map.get(self.arrow.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
            return loc_angle
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            loc_angle = static_from_layer2_angle_override_map.get(self.arrow.loc)
            if isinstance(loc_angle, dict):
                return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
            return loc_angle
