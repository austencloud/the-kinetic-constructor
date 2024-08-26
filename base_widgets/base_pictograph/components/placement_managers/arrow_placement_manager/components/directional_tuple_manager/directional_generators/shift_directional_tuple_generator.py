from data.constants import CLOCKWISE, PRO, ANTI
from .base_directional_tuple_generator import BaseDirectionalGenerator


class ShiftDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.motion_type == PRO:
            return self._generate_pro_directional_tuples(x, y)
        elif self.motion.motion_type == ANTI:
            return self._generate_anti_directional_tuples(x, y)

    def _generate_pro_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.prop_rot_dir == CLOCKWISE:
            return [(x, y), (-y, x), (-x, -y), (y, -x)]
        else:
            return [(-y, -x), (x, -y), (y, x), (-x, y)]

    def _generate_anti_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.prop_rot_dir == CLOCKWISE:
            return [(-y, -x), (x, -y), (y, x), (-x, y)]
        else:
            return [(x, y), (-y, x), (-x, -y), (y, -x)]
