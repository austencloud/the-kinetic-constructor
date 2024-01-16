from typing import List, Tuple
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    NO_ROT,
    PRO,
    ANTI,
    STATIC,
    SAME,
    OPP,
)
from objects.motion.motion import Motion


class DirectionalTupleGenerator:
    def __init__(self, motion: Motion, other_motion: Motion) -> None:
        self.motion = motion
        self.other_motion = other_motion

    def generate_directional_tuples(self, x: int, y: int) -> List[Tuple[int, int]]:
        motion_type = self.motion.motion_type
        prop_rot_dir = self.motion.prop_rot_dir

        if motion_type == DASH and self.motion.turns > 0:
            if self.motion.prop_rot_dir == self.other_motion.prop_rot_dir:
                self.motion.scene.vtg_timing = SAME
            elif self.motion.prop_rot_dir != self.other_motion.prop_rot_dir:
                self.motion.scene.vtg_timing = OPP

        shift_directional_tuples = {
            (PRO, CLOCKWISE): [(x, y), (-y, x), (-x, -y), (y, -x)],
            (PRO, COUNTER_CLOCKWISE): [(-y, -x), (x, -y), (y, x), (-x, y)],
            (ANTI, CLOCKWISE): [(-y, -x), (x, -y), (y, x), (-x, y)],
            (ANTI, COUNTER_CLOCKWISE): [(x, y), (-y, x), (-x, -y), (y, -x)],
        }

        pro_vs_no_rot_dash_directional_tuples = (
            [(x, y), (-y, x), (-x, -y), (y, -x)]
            if self.other_motion.prop_rot_dir == CLOCKWISE
            else [(-x, y), (-y, -x), (x, -y), (y, x)]  # COUNTER_CLOCKWISE
        )

        anti_vs_no_rot_dash_directional_tuples = (
            [(-x, y), (-y, -x), (x, -y), (y, x)]
            if self.other_motion.prop_rot_dir == CLOCKWISE
            else [(x, y), (-y, x), (-x, -y), (y, -x)]  # COUNTER_CLOCKWISE
        )

        no_rot_dash_vs_dash_directional_tuples = (
            [(x, y), (-y, x), (-x, -y), (y, -x)]
        )

        no_rot_dash_vs_static_directional_tuples = (
            [(x, y), (-y, x), (-x, -y), (y, -x)]
        )
        
        same_dash_directional_tuples = {
            (DASH, CLOCKWISE): ([(x, -y), (y, x), (-x, y), (-y, -x)]),
            (DASH, COUNTER_CLOCKWISE): ([(-x, -y), (y, -x), (x, y), (-y, x)]),
        }

        opp_dash_directional_tuples = {
            (DASH, CLOCKWISE): ([(x, -y), (y, x), (-x, y), (-y, -x)]),
            (DASH, COUNTER_CLOCKWISE): ([(-x, -y), (y, -x), (x, y), (-y, x)]),
        }

        no_rot_static_directional_tuples = [(x, -y), (y, x), (-x, y), (-y, -x)]

        static_directional_tuples = {
            (STATIC, CLOCKWISE): [(x, -y), (y, x), (-x, y), (-y, -x)],
            (STATIC, COUNTER_CLOCKWISE): [(-x, -y), (y, -x), (x, y), (-y, x)],
        }

        if (
            motion_type == DASH
            and prop_rot_dir == NO_ROT
            and self.other_motion.motion_type == PRO
        ):
            return pro_vs_no_rot_dash_directional_tuples
        elif (
            motion_type == DASH
            and prop_rot_dir == NO_ROT
            and self.other_motion.motion_type == ANTI
        ):
            return anti_vs_no_rot_dash_directional_tuples
        elif motion_type == DASH and prop_rot_dir == NO_ROT and self.other_motion.motion_type == DASH:
            return no_rot_dash_vs_dash_directional_tuples
        elif motion_type == DASH and prop_rot_dir == NO_ROT and self.other_motion.motion_type == STATIC:
            return no_rot_dash_vs_static_directional_tuples
        elif motion_type == DASH and self.motion.scene.vtg_timing == SAME:
            return same_dash_directional_tuples.get((motion_type, prop_rot_dir), [])
        elif motion_type == DASH and self.motion.scene.vtg_timing == OPP:
            return opp_dash_directional_tuples.get((motion_type, prop_rot_dir), [])
        elif motion_type == STATIC and prop_rot_dir == NO_ROT:
            return no_rot_static_directional_tuples
        elif motion_type == STATIC:
            return static_directional_tuples.get((motion_type, prop_rot_dir), [])
        else:
            return shift_directional_tuples.get((motion_type, prop_rot_dir), [])
