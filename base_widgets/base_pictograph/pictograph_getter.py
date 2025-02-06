from typing import TYPE_CHECKING, Optional
from Enums.Enums import LetterType, Letter, Glyph

from base_widgets.base_pictograph.grid.non_radial_points_group import (
    NonRadialPointsGroup,
)
from base_widgets.base_pictograph.lead_state_determiner import (
    LeadStateDeterminer,
)
from data.constants import *
from objects.arrow.arrow import Arrow
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographGetter:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph
        self.is_initialized = False

    def initiallize_getter(self):
        self.is_initialized = True
        self.blue_motion = self.pictograph.blue_motion
        self.red_motion = self.pictograph.red_motion
        self.blue_arrow = self.pictograph.blue_arrow
        self.red_arrow = self.pictograph.red_arrow
        self.lead_state_determiner = LeadStateDeterminer(
            self.red_motion, self.blue_motion
        )

    def motion_by_color(self, color: str) -> Motion:
        return self.pictograph.motions.get(color)

    def letter_type(self, letter: Letter) -> Optional[str]:
        letter_type_map = {
            letter: letter_type.description
            for letter_type in LetterType
            for letter in letter_type.letters
        }
        return letter_type_map.get(letter)

    def motions_by_type(self, motion_type: str) -> list[Motion]:
        return [
            motion
            for motion in self.pictograph.motions.values()
            if motion.motion_type == motion_type
        ]

    def trailing_motion(self) -> Motion:
        return self.lead_state_determiner.trailing_motion()

    def leading_motion(self) -> Motion:
        return self.lead_state_determiner.leading_motion()

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

    def float_motion(self) -> Motion:
        float_map = {True: self.red_motion, False: self.blue_motion}
        return float_map.get(self.red_motion.check.is_float())

    def opposite_location(self, loc: str) -> str:
        opposite_locations = {
            NORTH: SOUTH,
            SOUTH: NORTH,
            EAST: WEST,
            WEST: EAST,
            NORTHEAST: SOUTHWEST,
            SOUTHWEST: NORTHEAST,
            SOUTHEAST: NORTHWEST,
            NORTHWEST: SOUTHEAST,
        }
        return opposite_locations.get(loc)

    def turns_tuple(self) -> tuple[int, int, int]:
        generator = self.pictograph.main_widget.turns_tuple_generator
        return generator.generate_turns_tuple(self.pictograph)

    def pictograph_dict(self) -> dict:
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

    def glyphs(self) -> list[Glyph]:
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def non_radial_points(self) -> NonRadialPointsGroup:
        return self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial"
        )

    def glyph(self, name: str) -> Glyph:
        glyph_map = {
            "TKA": self.pictograph.tka_glyph,
            "VTG": self.pictograph.vtg_glyph,
            "Elemental": self.pictograph.elemental_glyph,
            "Positions": self.pictograph.start_to_end_pos_glyph,
            "Reversals": self.pictograph.reversal_glyph,
        }
        return glyph_map.get(name)
