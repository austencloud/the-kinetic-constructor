from typing import TYPE_CHECKING, Optional
from Enums.Enums import LetterType, Letter


from data.constants import *
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

    def motion_by_color(self, color: Color) -> Motion:
        return self.pictograph.motions.get(color)

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
        other_motion_map = {RED: self.blue_motion, BLUE: self.red_motion}
        return other_motion_map.get(motion.color)

    def other_arrow(self, arrow: Arrow) -> Arrow:
        other_arrow_map = {RED: self.blue_arrow, BLUE: self.red_arrow}
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
        # Adjusted to return nested attributes for blue and red
        return {
            "letter": self.pictograph.letter.value,
            "start_pos": self.pictograph.start_pos,
            "end_pos": self.pictograph.end_pos,
            "timing": self.pictograph.timing,
            "direction": self.pictograph.direction,
            "blue_attributes": {
                "motion_type": self.blue_motion.motion_type,
                "start_ori": self.blue_motion.start_ori,
                "prop_rot_dir": self.blue_motion.prop_rot_dir,
                "start_loc": self.blue_motion.start_loc,
                "end_loc": self.blue_motion.end_loc,
                "turns": self.blue_motion.turns,
                "end_ori": self.blue_motion.end_ori,
            },
            "red_attributes": {
                "motion_type": self.red_motion.motion_type,
                "start_ori": self.red_motion.start_ori,
                "prop_rot_dir": self.red_motion.prop_rot_dir,
                "start_loc": self.red_motion.start_loc,
                "end_loc": self.red_motion.end_loc,
                "turns": self.red_motion.turns,
                "end_ori": self.red_motion.end_ori,
            },
        }

    def end_pos_letter(self) -> str:
        """Check the end pos of the pictograph and if the string begins with "beta", return the lowercase beta symbol.
        If it's "alpha", return the lowercase alpha symbol.
        If it's "gamma", return the uppercase gamma symbol.
        """
        end_pos = self.pictograph.end_pos
        if end_pos.startswith("beta"):
            return "β"
        elif end_pos.startswith("alpha"):
            return "α"
        elif end_pos.startswith("gamma"):
            return "Γ"
        return end_pos

