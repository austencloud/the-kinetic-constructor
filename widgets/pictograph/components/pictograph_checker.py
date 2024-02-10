from typing import TYPE_CHECKING
from constants import *
from data.rules import beta_ending_letters, alpha_ending_letters, gamma_ending_letters

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographChecker:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def ends_in_beta(self) -> bool:
        return self.p.letter in beta_ending_letters

    def ends_in_alpha(self) -> bool:
        return self.p.letter in alpha_ending_letters

    def ends_in_gamma(self) -> bool:
        return self.p.letter in gamma_ending_letters

    def ends_in_hybrid_ori(self) -> bool:
        red_prop, blue_prop = self.p.props[RED], self.p.props[BLUE]
        return red_prop.check.is_radial() != blue_prop.check.is_radial()

    def ends_in_non_hybrid_ori(self) -> bool:
        red_prop, blue_prop = self.p.props[RED], self.p.props[BLUE]
        return (red_prop.check.is_radial() == blue_prop.check.is_radial()) or (
            red_prop.check.is_nonradial() and blue_prop.check.is_nonradial()
        )

    def ends_in_radial_ori(self) -> bool:
        return all(prop.check.is_radial() for prop in self.p.props.values())

    def ends_in_nonradial_ori(self) -> bool:
        return all(prop.check.is_nonradial() for prop in self.p.props.values())

    def has_a_dash(self) -> bool:
        for motion in self.p.motions.values():
            if motion.motion_type == DASH:
                return True
        return False

    def has_a_static_motion(self) -> bool:
        for motion in self.p.motions.values():
            if motion.motion_type == STATIC:
                return True
        return False

    def is_pictograph_dict_complete(self, pictograph_dict: dict) -> bool:
        required_keys = [
            "letter",
            "start_pos",
            "end_pos",
            "blue_motion_type",
            "blue_prop_rot_dir",
            "blue_start_loc",
            "blue_end_loc",
            "blue_start_ori",
            "blue_turns",
            "red_motion_type",
            "red_prop_rot_dir",
            "red_start_loc",
            "red_end_loc",
            "red_start_ori",
            "red_turns",
        ]
        return all(key in pictograph_dict for key in required_keys)

    def starts_from_mixed_orientation(self) -> bool:
        if (
            self.p.red_motion.start_ori in [CLOCK, COUNTER]
            and self.p.blue_motion.start_ori in [OUT, IN]
            or self.p.red_motion.start_ori in [OUT, IN]
            and self.p.blue_motion.start_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.p.red_motion.start_ori in [CLOCK, COUNTER]
            and self.p.blue_motion.start_ori in [CLOCK, COUNTER]
            or self.p.red_motion.start_ori in [OUT, IN]
            and self.p.blue_motion.start_ori in [OUT, IN]
        ):
            return False

    def starts_from_standard_orientation(self) -> bool:
        # return true if they're both radial or they're both nonradial start oris
        return (
            self.p.red_motion.start_ori in [IN, OUT]
            and self.p.blue_motion.start_ori in [IN, OUT]
        ) or (
            self.p.red_motion.start_ori in [CLOCK, COUNTER]
            and self.p.blue_motion.start_ori in [CLOCK, COUNTER]
        )

    def starts_from_radial_orientation(self) -> bool:
        return self.p.red_motion.start_ori in [
            IN,
            OUT,
        ] and self.p.blue_motion.start_ori in [IN, OUT]

    def starts_from_nonradial_orientation(self) -> bool:
        return self.p.red_motion.start_ori in [
            CLOCK,
            COUNTER,
        ] and self.p.blue_motion.start_ori in [CLOCK, COUNTER]

    def has_hybrid_motions(self) -> bool:
        return self.p.red_motion.motion_type != self.p.blue_motion.motion_type

    def is_in_sequence_builder(self) -> bool:
        # This method should return True if the application is in sequence builder mode.
        # Implement the logic based on your application's state management.
        return hasattr(self.p.scroll_area, "sequence_builder")