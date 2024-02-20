from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from Enums.PropTypes import PropType
from Enums.letters import LetterConditions, Letter
from constants import *

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographChecker:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def ends_with_beta(self) -> bool:

        return self.pictograph.letter in self.pictograph.letter.get_letters_by_condition(
            LetterConditions.BETA_ENDING
        )

    def ends_with_alpha(self) -> bool:
        return self.pictograph.letter in self.pictograph.letter.get_letters_by_condition(
            LetterConditions.ALPHA_ENDING
        )

    def ends_with_gamma(self) -> bool:
        return self.pictograph.letter in self.pictograph.letter.get_letters_by_condition(
            LetterConditions.GAMMA_ENDING
        )

    def ends_with_layer1(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[Color.RED],
            self.pictograph.props[Color.BLUE],
        )
        return red_prop.check.is_radial() == blue_prop.check.is_radial()

    def ends_with_layer2(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[Color.RED],
            self.pictograph.props[Color.BLUE],
        )
        return red_prop.check.is_nonradial() and blue_prop.check.is_nonradial()

    def ends_with_layer3(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[Color.RED],
            self.pictograph.props[Color.BLUE],
        )
        return red_prop.check.is_radial() != blue_prop.check.is_radial()

    def ends_with_non_hybrid_ori(self) -> bool:
        return self.ends_with_layer1() or self.ends_with_layer2()

    def ends_with_in_out_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[Color.RED],
            self.pictograph.props[Color.BLUE],
        )
        if red_prop.ori == IN and blue_prop.ori == OUT:
            return True
        elif red_prop.ori == OUT and blue_prop.ori == IN:
            return True
        return False

    def ends_with_clock_counter_ori(self) -> bool:
        red_prop, blue_prop = (
            self.pictograph.props[Color.RED],
            self.pictograph.props[Color.BLUE],
        )
        return (red_prop.ori in [CLOCK] and blue_prop.ori in [COUNTER]) or (
            red_prop.ori in [COUNTER] and blue_prop.ori in [CLOCK]
        )

    def ends_with_radial_ori(self) -> bool:
        return all(prop.check.is_radial() for prop in self.pictograph.props.values())

    def ends_with_nonradial_ori(self) -> bool:
        return all(prop.check.is_nonradial() for prop in self.pictograph.props.values())

    def has_a_dash(self) -> bool:
        for motion in self.pictograph.motions.values():
            if motion.motion_type == DASH:
                return True
        return False

    def has_a_static_motion(self) -> bool:
        for motion in self.pictograph.motions.values():
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
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [OUT, IN]
            or self.pictograph.red_motion.start_ori in [OUT, IN]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
        ):
            return True
        elif (
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
            or self.pictograph.red_motion.start_ori in [OUT, IN]
            and self.pictograph.blue_motion.start_ori in [OUT, IN]
        ):
            return False

    def starts_from_standard_orientation(self) -> bool:
        return (
            self.pictograph.red_motion.start_ori in [IN, OUT]
            and self.pictograph.blue_motion.start_ori in [IN, OUT]
        ) or (
            self.pictograph.red_motion.start_ori in [CLOCK, COUNTER]
            and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]
        )

    def starts_from_radial_orientation(self) -> bool:
        return self.pictograph.red_motion.start_ori in [
            IN,
            OUT,
        ] and self.pictograph.blue_motion.start_ori in [IN, OUT]

    def starts_from_nonradial_orientation(self) -> bool:
        return self.pictograph.red_motion.start_ori in [
            CLOCK,
            COUNTER,
        ] and self.pictograph.blue_motion.start_ori in [CLOCK, COUNTER]

    def has_hybrid_motions(self) -> bool:
        return (
            self.pictograph.red_motion.motion_type
            != self.pictograph.blue_motion.motion_type
        )

    def is_in_sequence_builder(self) -> bool:
        return hasattr(self.pictograph.scroll_area, "sequence_builder")

    def has_all_props_of_type(self, prop_type: PropType) -> bool:
        return all(
            prop.prop_type == prop_type for prop in self.pictograph.props.values()
        )

    def has_strictly_placed_props(self) -> bool:
        strict_props = [
            PropType.BigDoubleStar,
            PropType.BigHoop,
            PropType.BigBuugeng,
        ]
        return any(self.has_all_props_of_type(prop_type) for prop_type in strict_props)
