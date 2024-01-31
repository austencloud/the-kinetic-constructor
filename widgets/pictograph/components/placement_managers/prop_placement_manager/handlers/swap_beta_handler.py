from typing import TYPE_CHECKING
from Enums import LetterType
from objects.prop.prop import Prop

from utilities.TypeChecking.prop_types import *

if TYPE_CHECKING:
    from widgets.pictograph.components.placement_managers.prop_placement_manager.handlers.beta_prop_positioner import (
        BetaPropPositioner,
    )


class SwapBetaHandler:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.beta_prop_positioner = beta_prop_positioner
        self.pictograph = beta_prop_positioner.pictograph
        self.ppm = beta_prop_positioner.ppm
        self.blue_prop = self.pictograph.blue_prop
        self.red_prop = self.pictograph.red_prop

    def _swap_props(
        self, prop_a: Prop, prop_b: Prop, direction_a: str, direction_b: str
    ) -> None:
        self.beta_prop_positioner.move_prop(prop_a, direction_a)
        self.beta_prop_positioner.move_prop(prop_a, direction_a)
        self.beta_prop_positioner.move_prop(prop_b, direction_b)
        self.beta_prop_positioner.move_prop(prop_b, direction_b)

    def swap_beta(self) -> None:
        letter_type = LetterType.get_letter_type(self.pictograph.letter)

        if letter_type == Type1:
            self._handle_type1_swap()
        elif letter_type == Type2:
            self._handle_type2_swap()
        elif letter_type == Type3:
            self._handle_type3_swap()
        elif letter_type == Type4:
            self._handle_type4_swap()
        elif letter_type == Type5:
            self._handle_type5_swap()
        elif letter_type == Type6:
            self._handle_type6_swap()

    def _handle_type1_swap(self) -> None:
        red_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_direction = self.ppm.dir_calculator.get_dir(self.pictograph.blue_motion)

        self._swap_props(
            self.pictograph.red_prop,
            self.pictograph.blue_prop,
            blue_direction,
            red_direction,
        )

    def _handle_type6_swap(self) -> None:
        red_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_direction = self.ppm.dir_calculator.get_dir(self.pictograph.blue_motion)

        self._swap_props(
            self.pictograph.red_prop,
            self.pictograph.blue_prop,
            blue_direction,
            red_direction,
        )

    def _handle_type2_swap(self) -> None:
        shift = self.pictograph.get.shift()
        static = self.pictograph.get.static()

        shift_direction = self.ppm.dir_calculator.get_dir(shift)
        static_direction = self.ppm.dir_calculator.get_opposite_dir(shift_direction)

        self._swap_props(shift.prop, static.prop, static_direction, shift_direction)

    def _handle_type3_swap(self) -> None:
        shift = self.pictograph.get.shift()
        dash = self.pictograph.get.dash()

        direction = self.ppm.dir_calculator.get_dir(shift)

        if direction:
            self._swap_props(
                self.pictograph.props[shift.color],
                self.pictograph.props[dash.color],
                self.ppm.dir_calculator.get_opposite_dir(direction),
                direction,
            )

    def _handle_type4_swap(self) -> None:
        dash = self.pictograph.get.dash()
        static = self.pictograph.get.static()

        dash_direction = self.ppm.dir_calculator.get_dir(dash)
        static_direction = self.ppm.dir_calculator.get_opposite_dir(dash_direction)

        self._swap_props(dash.prop, static.prop, static_direction, dash_direction)

    def _handle_type5_swap(self) -> None:
        red_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        blue_direction = self.ppm.dir_calculator.get_dir(self.pictograph.blue_motion)

        self._swap_props(
            self.pictograph.red_prop,
            self.pictograph.blue_prop,
            blue_direction,
            red_direction,
        )

    def _generate_override_key(self, prop_loc, beta_ori) -> str:
        override_key = (
            f"swap_beta_{prop_loc}_{beta_ori}_"
            f"blue_{self.blue_prop.motion.motion_type}_{self.blue_prop.motion.arrow.loc}_"
            f"red_{self.red_prop.motion.motion_type}_{self.red_prop.motion.arrow.loc}"
        )

        return override_key

    def swap_beta_if_needed(self) -> None:
        ori_key = self.pictograph.arrow_placement_manager.special_positioner.data_updater._get_orientation_key(
            self.pictograph.blue_motion
        )

        if ori_key:
            letter_data: dict = self.pictograph.main_widget.special_placements[
                ori_key
            ].get(self.pictograph.letter)

        turns_tuple = self.pictograph.arrow_placement_manager.special_positioner.turns_tuple_generator.generate_turns_tuple(
            self.pictograph.letter
        )
        prop_loc = self.pictograph.blue_prop.loc
        if self.pictograph.check.ends_in_radial_ori():
            beta_ori = "radial"
        elif self.pictograph.check.ends_in_nonradial_ori():
            beta_ori = "nonradial"
        else:
            return
        override_key = self._generate_override_key(prop_loc, beta_ori)
        if letter_data:
            turn_data: dict = letter_data.get(turns_tuple, {})
            if beta_ori:
                if turn_data.get(override_key):
                    self.swap_beta()
