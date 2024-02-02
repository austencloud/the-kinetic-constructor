from typing import Callable
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    EAST,
    NO_ROT,
    NORTH,
    PRO,
    ANTI,
    RED,
    SOUTH,
    STATIC,
    WEST,
)
from objects.motion.motion import Motion
from utilities.TypeChecking.letter_lists import Type5_letters


class DirectionalTupleGenerator:
    def __init__(self, motion: Motion, other_motion: Motion) -> None:
        self.motion = motion
        self.other_motion = other_motion

    @property
    def _situations(
        self,
    ) -> dict[tuple[str, str, str], Callable[[int, int], list[tuple[int, int]]]]:
        return {
            (DASH, NO_ROT, PRO): self._pro_vs_no_rot_dash,
            (DASH, NO_ROT, ANTI): self._anti_vs_no_rot_dash,
            (STATIC, NO_ROT): self._no_rot_static,
            (STATIC,): self._static,
        }

    def generate_directional_tuples(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.pictograph.letter in Type5_letters and self.motion.turns == 0:
            return self._type5_zero_turns(x, y)
        situation = (
            self.motion.motion_type,
            self.motion.prop_rot_dir,
            self.other_motion.motion_type,
        )
        if situation in self._situations:
            return self._situations[situation](x, y)
        elif (
            self.motion.motion_type,
            self.motion.prop_rot_dir,
        ) in self._shift_directional_tuples:
            return self._shift_directional_tuples[
                (self.motion.motion_type, self.motion.prop_rot_dir)
            ](x, y)
        else:
            return self._default_case(x, y)

    def _default_case(self, x: int, y: int) -> list[tuple[int, int]]:
        if self.motion.motion_type == DASH and self.motion.prop_rot_dir == NO_ROT:
            if self.other_motion.motion_type == PRO:
                return self._pro_vs_no_rot_dash(x, y)
            elif self.other_motion.motion_type == ANTI:
                return self._anti_vs_no_rot_dash(x, y)
            elif self.other_motion.motion_type == STATIC:
                return self._no_rot_dash_vs_static(x, y)
        elif self.motion.motion_type == DASH:
            return self._dash(x, y)
        elif self.motion.motion_type == STATIC:
            if self.motion.prop_rot_dir == NO_ROT:
                return self._no_rot_static(x, y)
            else:
                return self._static(x, y)
        else:
            return []

    def _pro_vs_no_rot_dash(self, x: int, y: int) -> list[tuple[int, int]]:
        return (
            [(x, y), (-y, x), (-x, -y), (y, -x)]
            if self.other_motion.prop_rot_dir == CLOCKWISE
            else [(-x, y), (-y, -x), (x, -y), (y, x)]
        )

    def _anti_vs_no_rot_dash(self, x: int, y: int) -> list[tuple[int, int]]:
        return (
            [(-x, y), (-y, -x), (x, -y), (y, x)]
            if self.other_motion.prop_rot_dir == CLOCKWISE
            else [(x, y), (-y, x), (-x, -y), (y, -x)]
        )

    def _no_rot_dash_vs_static(self, x: int, y: int) -> list[tuple[int, int]]:
        return (
            [(x, y), (-y, x), (-x, -y), (y, -x)]
            if self.other_motion.prop_rot_dir == CLOCKWISE
            else [(-x, y), (-y, -x), (x, -y), (y, x)]
        )

    def _dash(self, x: int, y: int) -> list[tuple[int, int]]:
        return {
            (DASH, CLOCKWISE): [(x, -y), (y, x), (-x, y), (-y, -x)],
            (DASH, COUNTER_CLOCKWISE): [(-x, -y), (y, -x), (x, y), (-y, x)],
        }.get((self.motion.motion_type, self.motion.prop_rot_dir), [])

    def _no_rot_static(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(x, -y), (y, x), (-x, y), (-y, -x)]

    def _static(self, x: int, y: int) -> list[tuple[int, int]]:
        return {
            (STATIC, CLOCKWISE): [(x, -y), (y, x), (-x, y), (-y, -x)],
            (STATIC, COUNTER_CLOCKWISE): [(-x, -y), (y, -x), (x, y), (-y, x)],
        }.get((self.motion.motion_type, self.motion.prop_rot_dir), [])

    def _type5_zero_turns(self, x: int, y: int) -> list[tuple[int, int]]:
        Type5_zero_turns_directional_tuples = {
            (BLUE, (NORTH, SOUTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (BLUE, (EAST, WEST)): [(x, y), (-y, -x), (-x, -y), (y, x)],
            (BLUE, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (BLUE, (WEST, EAST)): [(x, y), (-y, -x), (-x, -y), (-y, x)],
            (RED, (NORTH, SOUTH)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (RED, (EAST, WEST)): [(x, y), (-y, -x), (-x, -y), (y, -x)],
            (RED, (SOUTH, NORTH)): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (RED, (WEST, EAST)): [(-x, y), (-y, -x), (-x, -y), (y, x)],
        }
        return Type5_zero_turns_directional_tuples.get(
            (self.motion.color, (self.motion.start_loc, self.motion.end_loc)), []
        )

    @property
    def _shift_directional_tuples(
        self,
    ) -> dict[tuple[str, str], Callable[[int, int], list[tuple[int, int]]]]:
        return {
            (PRO, CLOCKWISE): self._pro_clockwise,
            (PRO, COUNTER_CLOCKWISE): self._pro_counter_clockwise,
            (ANTI, CLOCKWISE): self._anti_clockwise,
            (ANTI, COUNTER_CLOCKWISE): self._anti_counter_clockwise,
        }

    def _pro_clockwise(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(x, y), (-y, x), (-x, -y), (y, -x)]

    def _pro_counter_clockwise(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(-y, -x), (x, -y), (y, x), (-x, y)]

    def _anti_clockwise(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(-y, -x), (x, -y), (y, x), (-x, y)]

    def _anti_counter_clockwise(self, x: int, y: int) -> list[tuple[int, int]]:
        return [(x, y), (-y, x), (-x, -y), (y, -x)]
