from data.constants import BOX, CLOCKWISE, COUNTER_CLOCKWISE, DIAMOND, NO_ROT
from .base_directional_tuple_generator import BaseDirectionalGenerator


class StaticDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        grid_mode = (
            self.motion.pictograph.main_widget.settings_manager.global_settings.get_grid_mode()
        )
        if grid_mode == DIAMOND:
            return self._generate_diamond_tuples(x, y)
        elif grid_mode == BOX:
            return self._generate_box_tuples(x, y)
        return []

    def _generate_diamond_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        direction_map = {
            CLOCKWISE: [(x, -y), (y, x), (-x, y), (-y, -x)],
            COUNTER_CLOCKWISE: [(-x, -y), (y, -x), (x, y), (-y, x)],
            NO_ROT: [(x, -y), (y, x), (-x, y), (-y, -x)],
        }
        return self._generate_tuples(x, y, direction_map)

    def _generate_box_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        direction_map = {
            CLOCKWISE: [(x, y), (-y, x), (-x, -y), (y, -x)],
            COUNTER_CLOCKWISE: [(-x, -y), (y, -x), (x, y), (-y, x)],
            NO_ROT: [(x, y), (-y, x), (-x, -y), (y, -x)],
        }
        return self._generate_tuples(x, y, direction_map)

    def _generate_tuples(
        self, x: int, y: int, direction_map: dict
    ) -> list[tuple[int, int]]:
        return direction_map.get(self.motion.prop_rot_dir, [])
