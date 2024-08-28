from data.constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class FloatRotAngleCalculator(BaseRotAngleCalculator):
    def calculate_angle(self):
        direction_map = self._float_direction_map()
        prop_rot_dir = self.arrow.motion.prop_rot_dir
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
                NORTHEAST: 270,
                SOUTHEAST: 180,
                SOUTHWEST: 90,
                NORTHWEST: 0,
            },
        }
