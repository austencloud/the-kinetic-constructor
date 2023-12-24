from typing import TYPE_CHECKING, Tuple, Callable, get_args


from PyQt6.QtCore import QPointF

from Enums import (
    AntiradialOrientation,
    Color,
    Direction,
    Location,
    MotionType,
    Orientation,
    RadialOrientation,
)
from constants.string_constants import ANTI, BLUE, CLOCK, COUNTER, EAST, IN, NORTH, NORTHEAST, NORTHWEST, OUT, PRO, RED, SOUTH, SOUTHEAST, SOUTHWEST, WEST

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.arrow_positioner import (
        ArrowPositioner,
    )
    from objects.arrow.arrow import Arrow


class StaffArrowPositioner:
    def __init__(
        self, pictograph: "Pictograph", arrow_positioner: "ArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.arrow_positioner = arrow_positioner

    def _adjust_arrows_for_staffs(self, current_letter) -> None:
        red_orientation = self.pictograph.motions[RED].prop.orientation
        blue_orientation = self.pictograph.motions[BLUE].prop.orientation

        # Mapping the letters to their respective methods
        letter_methods = {
            "K": self._adjust_arrows_for_letter_K,
            "L": self._adjust_arrows_for_letter_L,
            "H": self._adjust_arrows_for_letter_H,
            "I": self._adjust_arrows_for_letter_I,
            "Q": self._adjust_arrows_for_letter_Q,
            "R": self._adjust_arrows_for_letter_R,
            "V": self._adjust_arrows_for_letter_V,
        }

        # Call the corresponding method
        adjust_method = letter_methods.get(current_letter)
        if adjust_method:
            adjust_method(red_orientation, blue_orientation)

    # Methods for each letter with specific logic
    def _adjust_arrows_for_letter_K(self, red_orientation, blue_orientation) -> None:
        if self._are_both_props_radial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(90)

    def _adjust_arrows_for_letter_L(self, red_orientation, blue_orientation) -> None:
        self._apply_specific_arrow_adjustment(ANTI, OUT, 55)

        if self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            self._apply_adjustment_to_arrows_by_type(ANTI, 90)

    def _adjust_arrows_for_letter_H(self, red_orientation, blue_orientation) -> None:
        if self._are_both_props_radial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(90)

    def _adjust_arrows_for_letter_I(self, red_orientation, blue_orientation) -> None:
        if self._are_both_props_radial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(90)

    def _adjust_arrows_for_letter_Q(self, red_orientation, blue_orientation) -> None:
        if self._are_both_props_radial(red_orientation, blue_orientation):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_Q_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 60 if adjustment.x() < 0 else adjustment.x() + 60
                )
                adjusted_y = (
                    adjustment.y() - 60 if adjustment.y() < 0 else adjustment.y() + 60
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_R(self, red_orientation, blue_orientation) -> None:
        if self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_R_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 60 if adjustment.x() < 0 else adjustment.x() + 60
                )
                adjusted_y = (
                    adjustment.y() - 60 if adjustment.y() < 0 else adjustment.y() + 60
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_V(self, red_orientation, blue_orientation) -> None:
        if self._is_at_least_one_prop_antiradial(red_orientation, blue_orientation):
            anti_motion = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == ANTI
                else self.pictograph.motions[BLUE]
            )
            pro_motion = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == PRO
                else self.pictograph.motions[BLUE]
            )

            if anti_motion.prop.is_antiradial() and pro_motion.prop.is_radial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    anti_motion.arrow.location, 30
                )
                direction = self.get_antiradial_V_anti_adjustment_direction(
                    anti_motion.arrow.location,
                    anti_motion.end_location,
                    anti_motion.end_orientation,
                )
                if direction == Direction.UP:
                    adjustment += QPointF(0, -35)
                elif direction == Direction.DOWN:
                    adjustment += QPointF(0, 35)
                elif direction == Direction.LEFT:
                    adjustment += QPointF(-35, 0)
                elif direction == Direction.RIGHT:
                    adjustment += QPointF(35, 0)
                self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)
            else:
                # apply an equal adjustment of 90 to all ANTI arrows
                self._apply_adjustment_to_arrows_by_type(ANTI, 90)

    def get_antiradial_V_anti_adjustment_direction(
        self, arrow_location: str, end_location, orientation
    ) -> Callable:
        if orientation in [CLOCK, COUNTER]:
            if arrow_location == NORTHEAST:
                if end_location == EAST:
                    return Direction.DOWN
                elif end_location == NORTH:
                    return Direction.LEFT
            elif arrow_location == SOUTHEAST:
                if end_location == SOUTH:
                    return Direction.LEFT
                elif end_location == EAST:
                    return Direction.UP
            elif arrow_location == SOUTHWEST:
                if end_location == WEST:
                    return Direction.UP
                elif end_location == SOUTH:
                    return Direction.RIGHT
            elif arrow_location == NORTHWEST:
                if end_location == NORTH:
                    return Direction.RIGHT
                elif end_location == WEST:
                    return Direction.DOWN
        elif orientation in [IN, OUT]:
            if arrow_location == NORTHEAST:
                if end_location == EAST:
                    return Direction.LEFT
                elif end_location == NORTH:
                    return Direction.DOWN
            elif arrow_location == SOUTHEAST:
                if end_location == SOUTH:
                    return Direction.UP
                elif end_location == EAST:
                    return Direction.LEFT
            elif arrow_location == SOUTHWEST:
                if end_location == WEST:
                    return Direction.UP
                elif end_location == SOUTH:
                    return Direction.RIGHT
            elif arrow_location == NORTHWEST:
                if end_location == NORTH:
                    return Direction.RIGHT
                elif end_location == WEST:
                    return Direction.DOWN

    # Helper functions
    def _are_both_props_radial(self, red_orientation, blue_orientation) -> bool:
        return (
            red_orientation in RadialOrientation
            and blue_orientation in RadialOrientation
        )

    def _is_at_least_one_prop_antiradial(
        self, red_orientation, blue_orientation
    ) -> bool:
        return (
            red_orientation in AntiradialOrientation
            or blue_orientation in AntiradialOrientation
        )

    def _apply_adjustment_to_all_arrows(self, adjustment_value: int) -> None:
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)

    def _apply_specific_arrow_adjustment(
        self, motion_type: str, orientation: str, adjustment_value: int
    ) -> None:
        for arrow in self.pictograph.arrows.values():
            if (
                arrow.motion_type == motion_type
                and arrow.motion.prop.orientation == orientation
            ):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)

    def _apply_adjustment_to_arrows_by_type(
        self, motion_type: str, adjustment_value: int
    ) -> None:
        for arrow in self.pictograph.arrows.values():
            if arrow.motion_type == motion_type:
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.location, adjustment_value
                )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)
