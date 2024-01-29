from typing import TYPE_CHECKING
from Enums import LetterType
from constants import ANTI, PRO

from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import Directions
from utilities.TypeChecking.prop_types import *

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from ..prop_placement_manager import PropPlacementManager


class RepositionBetaPropsByLetterManager:
    def __init__(self, pictograph: "Pictograph", ppm: "PropPlacementManager"):
        self.pictograph = pictograph

        self.ppm = ppm
        self.red_prop = self.pictograph.red_prop
        self.blue_prop = self.pictograph.blue_prop

    def reposition_G_H(self) -> None:
        further_direction = self.ppm.dir_calculator.get_dir(self.pictograph.red_motion)
        other_direction = self.ppm.dir_calculator.get_opposite_dir(further_direction)
        self.move_prop(self.red_prop, further_direction)
        self.move_prop(self.blue_prop, other_direction)

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
        self.move_prop(pro_prop, pro_direction)
        self.move_prop(anti_prop, anti_direction)

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
