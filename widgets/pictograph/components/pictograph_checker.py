from typing import TYPE_CHECKING, Dict
from constants import *
from data.rules import beta_ending_letters, alpha_ending_letters, gamma_ending_letters
if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographChecker:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.p = pictograph

    def has_props_in_beta(self) -> bool:
        return self.p.letter.str in beta_ending_letters

    def has_props_in_alpha(self) -> bool:
        return self.p.letter.str in alpha_ending_letters

    def has_props_in_gamma(self) -> bool:
        return self.p.letter.str in gamma_ending_letters

    def has_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.p.props[RED], self.p.props[BLUE]
        return red_prop.check.is_radial() != blue_prop.check.is_radial()

    def has_non_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.p.props[RED], self.p.props[BLUE]
        return (red_prop.check.is_radial() == blue_prop.check.is_radial()) or (
            red_prop.check.is_antiradial() and blue_prop.check.is_antiradial()
        )

    def has_all_radial_props(self) -> bool:
        return all(prop.check.is_radial() for prop in self.p.props.values())

    def has_all_antiradial_props(self) -> bool:
        return all(prop.check.is_antiradial() for prop in self.p.props.values())

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

    def is_pictograph_dict_complete(self, pictograph_dict: Dict) -> bool:
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
