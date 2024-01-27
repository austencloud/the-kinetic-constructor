from typing import TYPE_CHECKING
from constants import ANTI, PRO

from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Directions
from utilities.TypeChecking.prop_types import *

if TYPE_CHECKING:
    from ..prop_placement_manager import PropPlacementManager


class BetaPropPositioner:
    def __init__(self, placement_manager: "PropPlacementManager") -> None:
        self.ppm = placement_manager
        self.pictograph = placement_manager.pictograph
        self.red_prop, self.blue_prop = (
            self.pictograph.red_prop,
            self.pictograph.blue_prop,
        )

    def reposition_beta_props(self) -> None:
        big_uni, small_uni, small_bi, big_bi = self._classify_props()

        if len(big_uni + big_bi) == 2:
            self._reposition_big_props(big_uni, big_bi)
        elif len(small_uni + small_bi) == 2:
            self._reposition_small_props(small_uni, small_bi)
        self.apply_swap_override_if_needed()

    def apply_swap_override_if_needed(self) -> None:
        if self.pictograph.blue_prop.motion.start_ori in [IN, OUT]:
            ori_key: str = "from_radial"
        elif self.pictograph.blue_prop.motion.start_ori in [CLOCK, COUNTER]:
            ori_key: str = "from_nonradial"
        else:
            return
        # Access the correct placements data based on the orientation
        if ori_key:
            letter_data: dict = self.pictograph.main_widget.special_placements[
                ori_key
            ].get(self.pictograph.letter)

        turns_tuple = self.pictograph.arrow_placement_manager.special_positioner.turns_tuple_generator.generate_turns_tuple(
            self.pictograph.letter
        )
        prop_loc = self.pictograph.blue_prop.loc
        if self.pictograph.check.has_all_radial_props():
            beta_ori = "radial"
        elif self.pictograph.check.has_all_nonradial_props():
            beta_ori = "nonradial"
        else:
            return
        override_key = (
            f"swap_beta_{prop_loc}_{beta_ori}_"
            f"blue_{self.blue_prop.motion.motion_type}_{self.blue_prop.motion.arrow.loc}_"
            f"red_{self.red_prop.motion.motion_type}_{self.red_prop.motion.arrow.loc}"
        )

        turn_data: dict = letter_data.get(turns_tuple, {})
        if beta_ori:
            if turn_data.get(override_key):
                self.swap_beta()

    def swap_beta(self) -> None:
        red_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_direction = self.ppm.dir_calculator.get_dir(self.pictograph.blue_motion)

        # move them double so they end up replacing each other's positions
        self.move_prop(self.red_prop, blue_direction)
        self.move_prop(self.red_prop, blue_direction)
        self.move_prop(self.blue_prop, red_direction)
        self.move_prop(self.blue_prop, red_direction)

    def _classify_props(self) -> tuple[list[Prop], list[Prop], list[Prop], list[Prop]]:
        props = self.pictograph.props.values()
        return (
            [p for p in props if p.prop_type in big_unilateral_prop_types],
            [p for p in props if p.prop_type in small_unilateral_prop_types],
            [p for p in props if p.prop_type in small_bilateral_prop_types],
            [p for p in props if p.prop_type in big_bilateral_prop_types],
        )

    def _reposition_small_bilateral_props(self) -> None:
        if self.pictograph.check.has_hybrid_orientations():
            for prop in self.pictograph.props.values():
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

        else:
            if self.pictograph.letter in ["G", "H"]:
                self.reposition_G_H()
            elif self.pictograph.letter == "I":
                self.reposition_I()
            elif self.pictograph.letter in ["J", "K", "L"]:
                self.reposition_J_K_L()
            elif self.pictograph.letter in ["Y", "Z"]:
                self.reposition_Y_Z()
            elif self.pictograph.letter == "β":
                self.reposition_β()
            elif self.pictograph.letter in ["Y-", "Z-"]:
                self.reposition_Y_dash_Z_dash()
            elif self.pictograph.letter == "Ψ":
                self.reposition_Ψ()
            elif self.pictograph.letter == "Ψ-":
                self.reposition_Ψ_dash()

    ### REPOSITIONING ###

    def _reposition_beta_props(self) -> None:
        big_unilateral_props: list[Prop] = [
            prop
            for prop in self.pictograph.props.values()
            if prop.prop_type in big_unilateral_prop_types
        ]
        small_unilateral_props: list[Prop] = [
            prop
            for prop in self.pictograph.props.values()
            if prop.prop_type in small_unilateral_prop_types
        ]
        small_bilateral_props: list[Prop] = [
            prop
            for prop in self.pictograph.props.values()
            if prop.prop_type in small_bilateral_prop_types
        ]
        big_bilateral_props: list[Prop] = [
            prop
            for prop in self.pictograph.props.values()
            if prop.prop_type in big_bilateral_prop_types
        ]
        big_props = big_unilateral_props + big_bilateral_props
        small_props = small_unilateral_props + small_bilateral_props
        if len(big_props) == 2:
            self._reposition_big_props(big_unilateral_props, big_bilateral_props)
        elif len(small_props) == 2:
            self._reposition_small_props(small_unilateral_props, small_bilateral_props)

    def _reposition_small_props(self, small_uni, small_bi) -> None:
        if len(small_uni) == 2:
            self._reposition_small_unilateral_props(small_uni)
        elif len(small_bi) == 2:
            self._reposition_small_bilateral_props()

    def _reposition_small_unilateral_props(self, small_uni: list[Prop]) -> None:
        if small_uni[0].ori == small_uni[1].ori:
            for prop in small_uni:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)
                red_direction = self.ppm.dir_calculator.get_dir(
                    self.pictograph.red_motion
                )
                blue_direction = self.ppm.dir_calculator.get_dir(
                    self.pictograph.blue_motion
                )
                self.move_prop(self.red_prop, red_direction)
                self.move_prop(self.blue_prop, blue_direction)
        else:
            for prop in small_uni:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

    def _reposition_big_props(
        self, big_unilateral_props: list[Prop], big_bilateral_props: list[Prop]
    ) -> None:
        big_props = big_unilateral_props + big_bilateral_props
        if self.pictograph.check.has_non_hybrid_orientations():
            for prop in big_props:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)
                (
                    red_direction,
                    blue_direction,
                ) = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
                self.move_prop(self.red_prop, red_direction)
                self.move_prop(self.blue_prop, blue_direction)
        else:
            for prop in big_props:
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

    def reposition_G_H(self) -> None:
        further_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        other_direction = self.ppm.dir_calculator.get_opposite_dir(further_direction)
        new_red_pos = self.ppm.offset_calculator.calculate_new_position_with_offset(
            self.red_prop.pos(), further_direction
        )
        new_blue_pos = self.ppm.offset_calculator.calculate_new_position_with_offset(
            self.blue_prop.pos(), other_direction
        )
        self.red_prop.setPos(new_red_pos)
        self.blue_prop.setPos(new_blue_pos)

    def reposition_I(self) -> None:
        pro_prop = (
            self.red_prop
            if self.pictograph.red_motion.motion_type == PRO
            else self.blue_prop
        )
        anti_prop = (
            self.red_prop
            if self.pictograph.red_motion.motion_type == ANTI
            else self.blue_prop
        )
        pro_motion = self.pictograph.motions[pro_prop.color]
        pro_direction = self.ppm.dir_calculator.get_dir(pro_motion)
        anti_direction = self.ppm.dir_calculator.get_opposite_dir(pro_direction)
        new_pro_position = (
            self.ppm.offset_calculator.calculate_new_position_with_offset(
                pro_prop.pos(), pro_direction
            )
        )
        new_anti_position = (
            self.ppm.offset_calculator.calculate_new_position_with_offset(
                anti_prop.pos(), anti_direction
            )
        )
        pro_prop.setPos(new_pro_position)
        anti_prop.setPos(new_anti_position)

    def reposition_J_K_L(self) -> None:
        red_dir = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_dir = self.ppm.dir_calculator.get_dir(self.pictograph.blue_motion)

        if red_dir and blue_dir:
            self.move_prop(self.red_prop, red_dir)
            self.move_prop(self.blue_prop, blue_dir)

    def reposition_Y_Z(self) -> None:
        shift = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_shift()
            else self.pictograph.blue_motion
        )
        static_motion = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_static()
            else self.pictograph.blue_motion
        )

        direction = self.ppm.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == shift.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == static_motion.color
                ),
                self.ppm.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Y_dash_Z_dash(self) -> None:
        shift = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_shift()
            else self.pictograph.blue_motion
        )
        dash = (
            self.pictograph.red_motion
            if self.pictograph.red_motion.check.is_dash()
            else self.pictograph.blue_motion
        )

        direction = self.ppm.dir_calculator.get_dir(shift)
        if direction:
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == shift.color
                ),
                direction,
            )
            self.move_prop(
                next(
                    prop
                    for prop in self.pictograph.props.values()
                    if prop.color == dash.color
                ),
                self.ppm.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Ψ(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.ppm.dir_calculator.get_dir_for_non_shift(self.red_prop)
            if direction:
                self.move_prop(self.red_prop, direction)
                self.move_prop(
                    self.blue_prop,
                    self.ppm.dir_calculator.get_opposite_dir(direction),
                )

        elif self.red_prop.prop_type in strictly_placed_props:
            self.ppm.default_positioner.set_prop_to_default_loc(self.red_prop)

    def reposition_Ψ_dash(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.ppm.dir_calculator.get_dir_for_non_shift(self.red_prop)
            if direction:
                self.move_prop(self.red_prop, direction)
                self.move_prop(
                    self.blue_prop,
                    self.ppm.dir_calculator.get_opposite_dir(direction),
                )

        elif self.red_prop.prop_type in strictly_placed_props:
            self.ppm.default_positioner.set_prop_to_default_loc()(self.red_prop)

    def reposition_β(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self.ppm.dir_calculator.get_dir_for_non_shift(self.red_prop)
            if direction:
                self.move_prop(self.red_prop, direction)
                self.move_prop(
                    self.blue_prop,
                    self.ppm.dir_calculator.get_opposite_dir(direction),
                )

        elif self.red_prop.prop_type in strictly_placed_props:
            self.ppm.default_positioner.set_prop_to_default_loc(self.red_prop)

    def move_prop(self, prop: Prop, direction: Directions) -> None:
        offset = self.ppm.offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
