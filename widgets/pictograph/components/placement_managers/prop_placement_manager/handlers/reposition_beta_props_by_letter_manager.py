from typing import TYPE_CHECKING
from constants import ANTI, PRO
from objects.prop.prop import Prop
from Enums.Enums import Directions

if TYPE_CHECKING:
    from .beta_prop_positioner import BetaPropPositioner


class RepositionBetaByLetterHandler:
    def __init__(self, beta_prop_positioner: "BetaPropPositioner") -> None:
        self.pictograph = beta_prop_positioner.pictograph
        self.prop_placement_manager = beta_prop_positioner.prop_placement_manager
        self.beta_prop_positioner = beta_prop_positioner

    def reposition_G_H(self) -> None:
        further_direction = self.prop_placement_manager.dir_calculator.get_dir(
            self.pictograph.red_motion
        )
        other_direction = self.prop_placement_manager.dir_calculator.get_opposite_dir(
            further_direction
        )
        self.move_prop(self.pictograph.red_prop, further_direction)
        self.move_prop(self.pictograph.blue_prop, other_direction)

    def reposition_I(self) -> None:
        pro_prop = (
            self.pictograph.red_prop
            if self.pictograph.red_motion.motion_type == PRO
            else self.pictograph.blue_prop
        )
        anti_prop = (
            self.pictograph.red_prop
            if self.pictograph.red_motion.motion_type == ANTI
            else self.pictograph.blue_prop
        )
        pro_motion = self.pictograph.motions[pro_prop.color]
        pro_direction = self.prop_placement_manager.dir_calculator.get_dir(pro_motion)
        anti_direction = self.prop_placement_manager.dir_calculator.get_opposite_dir(
            pro_direction
        )
        self.move_prop(pro_prop, pro_direction)
        self.move_prop(anti_prop, anti_direction)

    def reposition_J_K_L(self) -> None:

        red_dir = self.prop_placement_manager.dir_calculator.get_dir(
            self.pictograph.red_motion
        )
        blue_dir = self.prop_placement_manager.dir_calculator.get_dir(
            self.pictograph.blue_motion
        )

        if red_dir and blue_dir:
            self.move_prop(self.pictograph.red_prop, red_dir)
            self.move_prop(self.pictograph.blue_prop, blue_dir)

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

        direction = self.prop_placement_manager.dir_calculator.get_dir(shift)
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
                self.prop_placement_manager.dir_calculator.get_opposite_dir(direction),
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

        direction = self.prop_placement_manager.dir_calculator.get_dir(shift)
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
                self.prop_placement_manager.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Ψ(self) -> None:
        direction = self.prop_placement_manager.dir_calculator.get_dir_for_non_shift(
            self.pictograph.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.prop_placement_manager.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_Ψ_dash(self) -> None:

        direction = self.prop_placement_manager.dir_calculator.get_dir_for_non_shift(
            self.pictograph.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.prop_placement_manager.dir_calculator.get_opposite_dir(direction),
            )

    def reposition_β(self) -> None:
        direction = self.prop_placement_manager.dir_calculator.get_dir_for_non_shift(
            self.pictograph.red_prop
        )
        if direction:
            self.move_prop(self.pictograph.red_prop, direction)
            self.move_prop(
                self.pictograph.blue_prop,
                self.prop_placement_manager.dir_calculator.get_opposite_dir(direction),
            )

    def move_prop(self, prop: Prop, direction: Directions) -> None:
        offset = self.prop_placement_manager.offset_calculator.calculate_new_position_with_offset(
            prop.pos(), direction
        )
        prop.setPos(offset)
