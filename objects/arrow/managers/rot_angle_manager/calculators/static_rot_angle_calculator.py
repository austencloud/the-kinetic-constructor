from constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class StaticRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
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
