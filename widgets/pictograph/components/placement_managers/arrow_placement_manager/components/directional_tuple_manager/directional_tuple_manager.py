import logging
from constants import DASH, FLOAT, PRO, ANTI, STATIC
from objects.motion.motion import Motion
from .directional_generators.dash_directional_tuple_generator import (
    DashDirectionalGenerator,
)
from .directional_generators.shift_directional_tuple_generator import (
    ShiftDirectionalGenerator,
)
from .directional_generators.static_directional_tuple_generator import (
    StaticDirectionalGenerator,
)
from .directional_generators.base_directional_tuple_generator import (
    BaseDirectionalGenerator,
)


class DirectionalTupleManager:
    """
    TODO: Add docstring
    """

    def __init__(self, motion: Motion) -> None:
        self.generator: BaseDirectionalGenerator = self._select_generator(motion)

    def _select_generator(self, motion: Motion) -> "BaseDirectionalGenerator":
        if motion.motion_type in [PRO, ANTI, FLOAT]:
            return ShiftDirectionalGenerator(motion)
        elif motion.motion_type == DASH:
            return DashDirectionalGenerator(motion)
        elif motion.motion_type == STATIC:
            return StaticDirectionalGenerator(motion)
        else:
            logging.error(
                f"Can't find a directional tuple generator for motion type: {motion.motion_type}"
            )

    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        return self.generator.generate_directional_tuples(x, y)
