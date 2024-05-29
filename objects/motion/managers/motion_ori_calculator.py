from data.constants import *
from typing import TYPE_CHECKING
from Enums.MotionAttributes import Orientations, Location, MotionType
from Enums.Enums import Handpaths, Turns


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionOriCalculator:
    """Calculates the end orientation of a motion."""

    def __init__(self, motion: "Motion") -> None:
        self.motion = motion

    def get_end_ori(self) -> Orientations:
        if self.motion.motion_type == FLOAT:
            handpath_direction = self.get_handpath_direction(
                self.motion.start_loc, self.motion.end_loc
            )
            return self.calculate_float_orientation(
                self.motion.start_ori, handpath_direction
            )

        valid_turns = [0, 0.5, 1, 1.5, 2, 2.5, 3]
        if self.motion.turns in valid_turns:
            if self.motion.turns in [0, 1, 2, 3]:
                return self.calculate_whole_turn_orientation(
                    self.motion.motion_type, self.motion.turns, self.motion.start_ori
                )
            elif self.motion.turns in [0.5, 1.5, 2.5]:
                return self.calculate_half_turn_orientation(
                    self.motion.motion_type, self.motion.turns, self.motion.start_ori
                )

    def switch_orientation(self, ori: Orientations) -> Orientations:
        return {IN: OUT, OUT: IN, CLOCK: COUNTER, COUNTER: CLOCK}.get(ori, ori)

    def calculate_whole_turn_orientation(
        self, motion_type: MotionType, turns: Turns, start_ori: Orientations
    ) -> Orientations:
        if motion_type in [PRO, STATIC]:
            return start_ori if turns % 2 == 0 else self.switch_orientation(start_ori)
        elif motion_type in [ANTI, DASH]:
            return self.switch_orientation(start_ori) if turns % 2 == 0 else start_ori

    def calculate_half_turn_orientation(
        self, motion_type: MotionType, turns: Turns, start_ori: Orientations
    ) -> Orientations:
        if motion_type in [ANTI, DASH]:
            orientation_map = {
                (IN, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (IN, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (OUT, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (CLOCK, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (CLOCK, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (COUNTER, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
            }
        elif motion_type in [PRO, STATIC]:
            orientation_map = {
                (IN, CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (IN, COUNTER_CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, CLOCKWISE): (CLOCK if turns % 2 == 0.5 else COUNTER),
                (OUT, COUNTER_CLOCKWISE): (COUNTER if turns % 2 == 0.5 else CLOCK),
                (CLOCK, CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
                (CLOCK, COUNTER_CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, CLOCKWISE): (OUT if turns % 2 == 0.5 else IN),
                (COUNTER, COUNTER_CLOCKWISE): (IN if turns % 2 == 0.5 else OUT),
            }

        return orientation_map.get((start_ori, self.motion.prop_rot_dir))

    def calculate_float_orientation(
        self, start_ori: Orientations, handpath_direction: Handpaths
    ) -> Orientations:
        orientation_map = {
            (IN, CW_HANDPATH): COUNTER,
            (IN, CCW_HANDPATH): CLOCK,
            (OUT, CW_HANDPATH): CLOCK,
            (OUT, CCW_HANDPATH): COUNTER,
            (CLOCK, CW_HANDPATH): OUT,
            (CLOCK, CCW_HANDPATH): IN,
            (COUNTER, CW_HANDPATH): IN,
            (COUNTER, CCW_HANDPATH): OUT,
        }
        return orientation_map.get((start_ori, handpath_direction))

    def get_handpath_direction(
        self, start_loc: Location, end_loc: Location
    ) -> Handpaths:
        handpaths = {
            (NORTH, EAST): CW_HANDPATH,
            (EAST, SOUTH): CW_HANDPATH,
            (SOUTH, WEST): CW_HANDPATH,
            (WEST, NORTH): CW_HANDPATH,
            (NORTH, WEST): CCW_HANDPATH,
            (WEST, SOUTH): CCW_HANDPATH,
            (SOUTH, EAST): CCW_HANDPATH,
            (EAST, NORTH): CCW_HANDPATH,
            (NORTH, SOUTH): DASH_HANDPATH,
            (SOUTH, NORTH): DASH_HANDPATH,
            (EAST, WEST): DASH_HANDPATH,
            (WEST, EAST): DASH_HANDPATH,
            (NORTH, NORTH): STATIC_HANDPATH,
            (SOUTH, SOUTH): STATIC_HANDPATH,
            (EAST, EAST): STATIC_HANDPATH,
            (WEST, WEST): STATIC_HANDPATH,
        }
        return handpaths.get((start_loc, end_loc), STATIC_HANDPATH)
