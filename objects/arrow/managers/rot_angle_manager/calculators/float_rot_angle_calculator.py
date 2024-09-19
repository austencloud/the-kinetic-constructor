from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class FloatRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        direction_map = self._float_direction_map()
        loc = self.arrow.loc
        handpath_direction = self.arrow.motion.ori_calculator.get_handpath_direction(
            self.arrow.motion.start_loc, self.arrow.motion.end_loc
        )
        return direction_map.get(handpath_direction, {}).get(loc, 0)

    def _float_direction_map(self):
        return {
            CW_HANDPATH: {
                NORTHEAST: 0,
                SOUTHEAST: 90,
                SOUTHWEST: 180,
                NORTHWEST: 270,
            },
            CCW_HANDPATH: {
                NORTHEAST: 180,
                SOUTHEAST: 270,
                SOUTHWEST: 0,
                NORTHWEST: 90,
            },
        }
