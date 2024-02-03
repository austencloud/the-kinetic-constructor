from constants import *
from .base_rot_angle_calculator import BaseRotAngleCalculator


class ProRotAngleCalculator(BaseRotAngleCalculator):
    def _calculate_angle_impl(self):
        direction_map = self._pro_direction_map()
        prop_rot_dir = self.arrow.motion.prop_rot_dir
        loc = self.arrow.loc
        return direction_map.get(prop_rot_dir, {}).get(loc, 0)

    def _pro_direction_map(self):
        return {
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
