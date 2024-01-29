from typing import TYPE_CHECKING
from Enums import LetterType
from constants import ANTI, PRO

from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Directions
from utilities.TypeChecking.prop_types import *
from widgets.pictograph.components.placement_managers.prop_placement_manager.handlers.reposition_beta_props_by_letter_manager import (
    RepositionBetaPropsByLetterManager,
)

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from ..prop_placement_manager import PropPlacementManager


class BetaPropPositioner:
    def __init__(self, ppm: "PropPlacementManager") -> None:
        self.pictograph = ppm.pictograph
        self.ppm = ppm
        self.red_prop = self.pictograph.red_prop
        self.blue_prop = self.pictograph.blue_prop
        self.reposition_beta_props_by_letter_manager = (
            RepositionBetaPropsByLetterManager(self.pictograph, self.ppm)
        )

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

    def _reposition_small_bilateral_props(self) -> None:
        if self.pictograph.check.has_hybrid_orientations():
            for prop in self.pictograph.props.values():
                self.ppm.default_positioner.set_prop_to_default_loc(prop)

        else:
            if self.pictograph.letter in ["G", "H"]:
                self.reposition_beta_props_by_letter_manager.reposition_G_H()
            elif self.pictograph.letter == "I":
                self.reposition_beta_props_by_letter_manager.reposition_I()
            elif self.pictograph.letter in ["J", "K", "L"]:
                self.reposition_beta_props_by_letter_manager.reposition_J_K_L()
            elif self.pictograph.letter in ["Y", "Z"]:
                self.reposition_beta_props_by_letter_manager.reposition_Y_Z()
            elif self.pictograph.letter == "β":
                self.reposition_beta_props_by_letter_manager.reposition_β()
            elif self.pictograph.letter in ["Y-", "Z-"]:
                self.reposition_beta_props_by_letter_manager.reposition_Y_dash_Z_dash()
            elif self.pictograph.letter == "Ψ":
                self.reposition_beta_props_by_letter_manager.reposition_Ψ()
            elif self.pictograph.letter == "Ψ-":
                self.reposition_beta_props_by_letter_manager.reposition_Ψ_dash()

    def move_prop(self, prop: Prop, direction: Directions) -> None:
        offset = self.ppm.offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)

    def _classify_props(self) -> tuple[list[Prop], list[Prop], list[Prop], list[Prop]]:
        props = self.pictograph.props.values()
        return (
            [p for p in props if p.prop_type in big_unilateral_prop_types],
            [p for p in props if p.prop_type in small_unilateral_prop_types],
            [p for p in props if p.prop_type in small_bilateral_prop_types],
            [p for p in props if p.prop_type in big_bilateral_prop_types],
        )

    def swap_beta(self) -> None:
        if LetterType.get_letter_type(self.pictograph.letter) == Type1:
            red_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
            blue_direction = self.ppm.dir_calculator.get_dir(
                self.pictograph.blue_motion
            )
            self.move_prop(self.red_prop, blue_direction)
            self.move_prop(self.red_prop, blue_direction)
            self.move_prop(self.blue_prop, red_direction)
            self.move_prop(self.blue_prop, red_direction)

        elif LetterType.get_letter_type(self.pictograph.letter) == Type2:
            shift = self.pictograph.get.shift()
            static = self.pictograph.get.static()
            shift_direction = self.ppm.dir_calculator.get_dir(shift)
            static_direction = self.ppm.dir_calculator.get_opposite_dir(shift_direction)
            self.move_prop(shift.prop, static_direction)
            self.move_prop(static.prop, shift_direction)
            self.move_prop(shift.prop, static_direction)
            self.move_prop(static.prop, shift_direction)

        elif LetterType.get_letter_type(self.pictograph.letter) == Type3:
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
                    self.ppm.dir_calculator.get_opposite_dir(direction),
                )
                self.move_prop(
                    next(
                        prop
                        for prop in self.pictograph.props.values()
                        if prop.color == dash.color
                    ),
                    direction,
                )
                self.move_prop(
                    next(
                        prop
                        for prop in self.pictograph.props.values()
                        if prop.color == shift.color
                    ),
                    self.ppm.dir_calculator.get_opposite_dir(direction),
                )
                self.move_prop(
                    next(
                        prop
                        for prop in self.pictograph.props.values()
                        if prop.color == dash.color
                    ),
                    direction,
                )

    def _generate_ori_key(self) -> str:
        if self.pictograph.blue_prop.motion.start_ori in [IN, OUT]:
            ori_key: str = "from_radial"
        elif self.pictograph.blue_prop.motion.start_ori in [CLOCK, COUNTER]:
            ori_key: str = "from_nonradial"
        return ori_key

    def _generate_override_key(self, prop_loc, beta_ori) -> str:
        override_key = (
            f"swap_beta_{prop_loc}_{beta_ori}_"
            f"blue_{self.blue_prop.motion.motion_type}_{self.blue_prop.motion.arrow.loc}_"
            f"red_{self.red_prop.motion.motion_type}_{self.red_prop.motion.arrow.loc}"
        )

        return override_key

    def apply_swap_override_if_needed(self) -> None:
        ori_key = self._generate_ori_key()

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
        override_key = self._generate_override_key(prop_loc, beta_ori)
        if letter_data:
            turn_data: dict = letter_data.get(turns_tuple, {})
            if beta_ori:
                if turn_data.get(override_key):
                    self.swap_beta()

    def reposition_beta_props(self) -> None:
        self._reposition_beta_props()
        self.apply_swap_override_if_needed()
