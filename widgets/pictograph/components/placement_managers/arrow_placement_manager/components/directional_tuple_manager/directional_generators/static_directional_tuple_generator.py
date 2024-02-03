from constants import CLOCKWISE, COUNTER_CLOCKWISE, NO_ROT
from .base_directional_tuple_generator import BaseDirectionalGenerator


class StaticDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.prop_rot_dir == CLOCKWISE:
            return [(x, -y), (y, x), (-x, y), (-y, -x)]
        elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return [(-x, -y), (y, -x), (x, y), (-y, x)]
        elif self.motion.prop_rot_dir == NO_ROT:
            return [(x, -y), (y, x), (-x, y), (-y, -x)]
        
