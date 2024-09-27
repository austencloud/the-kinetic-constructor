from typing import TYPE_CHECKING
from Enums.MotionAttributes import Location, MotionType
from Enums.Enums import Handpaths, Turns
from data.constants import (
    ANTI,
    CLOCK,
    COUNTER,
    CW_HANDPATH,
    CCW_HANDPATH,
    DASH,
    DASH_HANDPATH,
    PRO,
    STATIC,
    STATIC_HANDPATH,
    IN,
    OUT,
    FLOAT,
    NORTH,
    EAST,
    SOUTH,
    WEST,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
)
from objects.motion.managers.hand_rotation_direction_calculator import (
    HandRotationDirectionCalculator,
)


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionOriCalculator:
    """Calculates the end orientation of a motion."""

    def __init__(self, motion: "Motion") -> None:
        self.motion = motion
        self.hand_rot_dir_calculator = HandRotationDirectionCalculator()

    def get_end_ori(self) -> str:
        if self.motion.motion_type == FLOAT:  # Handle float case
            handpath_direction = (
                self.hand_rot_dir_calculator.get_hand_rot_dir_from_locs(
                    self.motion.start_loc, self.motion.end_loc
                )
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

    def switch_orientation(self, ori: str) -> str:
        return {IN: OUT, OUT: IN, CLOCK: COUNTER, COUNTER: CLOCK}.get(ori, ori)

    def calculate_whole_turn_orientation(
        self, motion_type: MotionType, turns: Turns, start_ori: str
    ) -> str:
        if motion_type in [PRO, STATIC]:
            return start_ori if turns % 2 == 0 else self.switch_orientation(start_ori)
        elif motion_type in [ANTI, DASH]:
            return self.switch_orientation(start_ori) if turns % 2 == 0 else start_ori

    def calculate_half_turn_orientation(
        self, motion_type: MotionType, turns: Turns, start_ori: str
    ) -> str:
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
        self, start_ori: str, handpath_direction: Handpaths
    ) -> str:
        orientation_map = {
            (IN, CLOCKWISE): CLOCK,
            (IN, COUNTER_CLOCKWISE): COUNTER,
            (OUT, CLOCKWISE): COUNTER,
            (OUT, COUNTER_CLOCKWISE): CLOCK,
            (CLOCK, CLOCKWISE): OUT,
            (CLOCK, COUNTER_CLOCKWISE): IN,
            (COUNTER, CLOCKWISE): IN,
            (COUNTER, COUNTER_CLOCKWISE): OUT,
        }
        return orientation_map.get((start_ori, handpath_direction))

