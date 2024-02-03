from constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class DashRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        if self.arrow.motion.prop_rot_dir == NO_ROT:
            return self._handle_no_rotation()

        return self._handle_orientation_based_rotation()

    def _handle_no_rotation(self):
        no_rotation_map = {
            (NORTH, SOUTH): 90,
            (EAST, WEST): 180,
            (SOUTH, NORTH): 270,
            (WEST, EAST): 0,
        }
        return no_rotation_map.get(
            (self.arrow.motion.start_loc, self.arrow.motion.end_loc), 0
        )

    def _handle_orientation_based_rotation(self):
        orientation_rotation_map = {
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
            },
            COUNTER: {
                CLOCKWISE: {NORTH: 0, EAST: 90, SOUTH: 180, WEST: 270},
                COUNTER_CLOCKWISE: {NORTH: 0, EAST: 270, SOUTH: 180, WEST: 90},
            },
        }

        start_ori_map = orientation_rotation_map.get(self.arrow.motion.start_ori, {})
        rotation_map = start_ori_map.get(self.arrow.motion.prop_rot_dir, {})

        return rotation_map.get(self.arrow.loc, 0)
