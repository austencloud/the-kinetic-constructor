from typing import TYPE_CHECKING, Optional
from Enums import Letter, LetterType

from constants import *
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from utilities.TypeChecking.MotionAttributes import Locations, MotionTypes


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographGetter:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def letter_type(self, letter: Letter) -> Optional[str]:
        for letter_type in LetterType:
            if letter in letter_type.letters:
                return letter_type.description
        return None

    def motions_by_type(self, motion_type: MotionTypes) -> list[Motion]:
        return [
            motion
            for motion in self.p.motions.values()
            if motion.motion_type == motion_type
        ]

    def leading_motion(self) -> Motion:
        if self.p.red_motion.start_loc and self.p.blue_motion.start_loc:
            if self.p.red_motion.start_loc == self.p.blue_motion.end_loc:
                return self.p.red_motion
            elif self.p.blue_motion.start_loc == self.p.red_motion.end_loc:
                return self.p.blue_motion
        else:
            return None

    def trailing_motion(self) -> Motion:
        if self.p.red_motion.start_loc == self.p.blue_motion.end_loc:
            return self.p.blue_motion
        elif self.p.blue_motion.start_loc == self.p.red_motion.end_loc:
            return self.p.red_motion

    def other_motion(self, motion: Motion) -> Motion:
        if motion.color == RED:
            return self.p.blue_motion
        elif motion.color == BLUE:
            return self.p.red_motion

    def other_arrow(self, arrow: Arrow) -> Arrow:
        if arrow.color == RED:
            return self.p.blue_arrow
        elif arrow.color == BLUE:
            return self.p.red_arrow

    def dash(self) -> Motion:
        return self.p.motions[RED if self.p.red_motion.check.is_dash() else BLUE]

    def shift(self) -> Motion:
        return self.p.motions[RED if self.p.red_motion.check.is_shift() else BLUE]

    def static(self) -> Motion:
        return self.p.motions[RED if self.p.red_motion.check.is_static() else BLUE]

    def opposite_location(self, loc: Locations) -> Locations:
        opposite_locations = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_locations.get(loc)
