from typing import TYPE_CHECKING, Optional
from Enums.Enums import LetterType, Letter


from constants import *
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion
from Enums.MotionAttributes import Color, Location, MotionType


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographGetter:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.is_initialized = False

    def initiallize_getter(self):
        self.is_initialized = True
        self.blue_motion = self.pictograph.blue_motion
        self.red_motion = self.pictograph.red_motion
        self.blue_arrow = self.pictograph.blue_arrow
        self.red_arrow = self.pictograph.red_arrow
        self.turns_tuple_generator = self.pictograph.main_widget.turns_tuple_generator

    def letter_type(self, letter: Letter) -> Optional[str]:
        letter_type_map = {
            letter: letter_type.description
            for letter_type in LetterType
            for letter in letter_type.letters
        }
        return letter_type_map.get(letter)

    def motions_by_type(self, motion_type: MotionType) -> list[Motion]:
        return [
            motion
            for motion in self.pictograph.motions.values()
            if motion.motion_type == motion_type
        ]

    def leading_motion(self) -> Motion:
        red_start = self.red_motion.start_loc
        blue_end = self.blue_motion.end_loc
        blue_start = self.blue_motion.start_loc
        red_end = self.red_motion.end_loc

        motion_map = {
            (red_start, blue_end): self.red_motion,
            (blue_start, red_end): self.blue_motion,
        }
        return motion_map.get((self.red_motion.start_loc, self.blue_motion.end_loc))

    def trailing_motion(self) -> Motion:
        red_start = self.red_motion.start_loc
        blue_end = self.blue_motion.end_loc
        blue_start = self.blue_motion.start_loc
        red_end = self.red_motion.end_loc

        motion_map = {
            (red_start, blue_end): self.blue_motion,
            (blue_start, red_end): self.red_motion,
        }
        return motion_map.get((self.red_motion.start_loc, self.blue_motion.end_loc))

    def other_motion(self, motion: Motion) -> Motion:
        other_motion_map = {Color.RED: self.blue_motion, Color.BLUE: self.red_motion}
        return other_motion_map.get(motion.color)

    def other_arrow(self, arrow: Arrow) -> Arrow:
        other_arrow_map = {Color.RED: self.blue_arrow, Color.BLUE: self.red_arrow}
        return other_arrow_map.get(arrow.color)

    def dash(self) -> Motion:
        dash_map = {True: self.red_motion, False: self.blue_motion}
        return dash_map.get(self.red_motion.check.is_dash())

    def shift(self) -> Motion:
        shift_map = {True: self.red_motion, False: self.blue_motion}
        return shift_map.get(self.red_motion.check.is_shift())

    def static(self) -> Motion:
        static_map = {True: self.red_motion, False: self.blue_motion}
        return static_map.get(self.red_motion.check.is_static())

    def opposite_location(self, loc: Location) -> Location:
        opposite_locations = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
        return opposite_locations.get(loc)

    def turns_tuple(self) -> tuple[int, int, int]:
        return self.turns_tuple_generator.generate_turns_tuple(self.pictograph)

    def pictograph_dict(self) -> dict:
        return {
            "letter": self.pictograph.letter.value,
            "start_pos": self.pictograph.start_pos,
            "end_pos": self.pictograph.end_pos,
            "blue_motion_type": self.blue_motion.motion_type,
            "blue_start_ori": self.blue_motion.start_ori,
            "blue_prop_rot_dir": self.blue_motion.prop_rot_dir,
            "blue_start_loc": self.blue_motion.start_loc,
            "blue_end_loc": self.blue_motion.end_loc,
            "red_motion_type": self.red_motion.motion_type,
            "red_start_ori": self.red_motion.start_ori,
            "red_prop_rot_dir": self.red_motion.prop_rot_dir,
            "red_start_loc": self.red_motion.start_loc,
            "red_end_loc": self.red_motion.end_loc,
            "blue_turns": self.blue_motion.turns,
            "red_turns": self.red_motion.turns,
            "blue_end_ori": self.blue_motion.end_ori,
            "red_end_ori": self.red_motion.end_ori,
        }
