from Enums.Enums import LetterType
from Enums.MotionAttributes import Color
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    EAST,
    NO_ROT,
    NORTH,
    PRO,
    ANTI,
    SOUTH,
    STATIC,
    WEST,
)
from .base_directional_tuple_generator import BaseDirectionalGenerator


class DashDirectionalGenerator(BaseDirectionalGenerator):
    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if (
            self.motion.pictograph.letter_type == LetterType.Type5
            and self.motion.turns == 0
        ):
            return self._handle_type5_zero_turns(x, y)

        elif self.motion.prop_rot_dir == NO_ROT:
            return self._handle_no_rotation_dash(x, y)
        elif self.motion.prop_rot_dir == CLOCKWISE:
            return [(x, -y), (y, x), (-x, y), (-y, -x)]
        elif self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return [(-x, -y), (y, -x), (x, y), (-y, x)]

    def _handle_no_rotation_dash(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.other_motion.motion_type == PRO:
            return (
                [(x, y), (-y, x), (-x, -y), (y, -x)]
                if self.other_motion.prop_rot_dir == CLOCKWISE
                else [(-x, y), (-y, -x), (x, -y), (y, x)]
            )
        elif self.other_motion.motion_type == ANTI:
            return (
                [(-x, y), (-y, -x), (x, -y), (y, x)]
                if self.other_motion.prop_rot_dir == CLOCKWISE
                else [(x, y), (-y, x), (-x, -y), (y, -x)]
            )
        elif self.other_motion.motion_type == STATIC:
            if self.other_motion.prop_rot_dir == CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif self.other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]

        elif self.other_motion.motion_type == DASH:
            if self.other_motion.prop_rot_dir == CLOCKWISE:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]
            elif self.other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                return [(-x, -y), (y, -x), (x, y), (-y, x)]
            else:
                return [(x, -y), (y, x), (-x, y), (-y, -x)]

    def _handle_type5_zero_turns(self, x: int, y: int) -> list[tuple[int, int]]:
        Type5_zero_turns_directional_tuples = {
            (Color.BLUE, (NORTH, SOUTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (Color.BLUE, (EAST, WEST)): [(x, y), (-y, -x), (-x, -y), (y, x)],
            (Color.BLUE, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (Color.BLUE, (WEST, EAST)): [(x, y), (-y, -x), (-x, -y), (-y, x)],
            (Color.RED, (NORTH, SOUTH)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (Color.RED, (EAST, WEST)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (Color.RED, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (Color.RED, (WEST, EAST)): [(-x, y), (-y, -x), (-x, -y), (y, x)],
        }
        return Type5_zero_turns_directional_tuples.get(
            (self.motion.color, (self.motion.start_loc, self.motion.end_loc)), []
        )
