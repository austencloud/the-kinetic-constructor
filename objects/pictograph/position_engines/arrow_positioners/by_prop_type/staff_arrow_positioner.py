from typing import TYPE_CHECKING, Literal
from PyQt6.QtCore import QPointF
from Enums import (
    AntiradialOrientation,
    Color,
    RadialOrientation,
)
from constants import (
    ANTI,
    BLUE,
    DOWN,
    EAST,
    LEFT,
    NORTH,
    NORTHEAST,
    NORTHWEST,
    OUT,
    PRO,
    RED,
    RIGHT,
    SOUTH,
    SOUTHEAST,
    SOUTHWEST,
    UP,
    WEST,
    DISTANCE,
)
from objects.motion import Motion


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.base_arrow_positioner import (
        BaseArrowPositioner,
    )


class StaffArrowPositioner:
    def __init__(
        self, pictograph: "Pictograph", arrow_positioner: "BaseArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.arrow_positioner = arrow_positioner

    def _adjust_arrows_for_staffs(self, current_letter) -> None:
        red_motion = self.pictograph.motions[RED]
        blue_motion = self.pictograph.motions[BLUE]

        # Mapping the letters to their respective methods
        letter_methods = {
            "K": self._adjust_arrows_for_letter_K,
            "L": self._adjust_arrows_for_letter_L,
            "H": self._adjust_arrows_for_letter_H,
            "I": self._adjust_arrows_for_letter_I,
            "Q": self._adjust_arrows_for_letter_Q,
            "R": self._adjust_arrows_for_letter_R,
            "T": self._adjust_arrows_for_letter_T,
            "U": self._adjust_arrows_for_letter_U,
            "V": self._adjust_arrows_for_letter_V,
            "X": self._adjust_arrows_for_letter_X,
            "Z": self._adjust_arrows_for_letter_Z,
        }

        # Call the corresponding method
        adjust_method = letter_methods.get(current_letter)
        if adjust_method:
            adjust_method(red_motion, blue_motion)

    # Methods for each letter with specific logic
    def _adjust_arrows_for_letter_K(self, red_motion, blue_motion) -> None:
        if self._are_both_props_radial(red_motion, blue_motion):
            self._apply_adjustment_to_all_arrows(55)

        elif self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            self._apply_adjustment_to_all_arrows(90)

    def _adjust_arrows_for_letter_L(self, red_motion, blue_motion) -> None:
        self._apply_specific_arrow_adjustment(ANTI, OUT, 55)

        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            self._apply_adjustment_to_arrows_by_type(ANTI, 90)

    def _adjust_arrows_for_letter_H(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_GH_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 30 if adjustment.x() < 0 else adjustment.x() + 30
                )
                adjusted_y = (
                    adjustment.y() - 30 if adjustment.y() < 0 else adjustment.y() + 30
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_I(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            for arrow in self.pictograph.arrows.values():
                adjustment = self.arrow_positioner._calculate_I_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 30 if adjustment.x() < 0 else adjustment.x() + 30
                )
                adjusted_y = (
                    adjustment.y() - 30 if adjustment.y() < 0 else adjustment.y() + 30
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_adjustment(arrow, adjusted_adjustment)

    def _adjust_arrows_for_letter_Q(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
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

    def _adjust_arrows_for_letter_R(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
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

    def _adjust_arrows_for_letter_T(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            leading_color: Color = self.determine_leading_motion_for_T(
                self.pictograph.motions[RED].start_loc,
                self.pictograph.motions[RED].end_loc,
                self.pictograph.motions[BLUE].start_loc,
                self.pictograph.motions[BLUE].end_loc,
            )
            leader = self.pictograph.motions[leading_color]
            if leading_color == RED:
                follower = self.pictograph.motions[BLUE]
            else:
                follower = self.pictograph.motions[RED]

            for arrow in self.pictograph.arrows.values():
                if arrow.motion.prop.is_antiradial():
                    default_pos = self.arrow_positioner._get_default_position(arrow)
                    adjustment = self.arrow_positioner.calculate_adjustment(
                        arrow.location, DISTANCE + -45
                    )
                    new_pos = default_pos + adjustment - arrow.boundingRect().center()
                    arrow.setPos(new_pos)

            if leader.prop.is_antiradial() and follower.prop.is_radial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    leader.arrow.location, 30
                )
                direction = self.get_antispin_antiradial_adjustment_direction(leader)
                if direction == UP:
                    adjustment += QPointF(0, -40)
                elif direction == DOWN:
                    adjustment += QPointF(0, 40)
                elif direction == LEFT:
                    adjustment += QPointF(-40, 0)
                elif direction == RIGHT:
                    adjustment += QPointF(40, 0)
                self.arrow_positioner._apply_adjustment(leader.arrow, adjustment)

            elif leader.prop.is_radial() and follower.prop.is_antiradial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    follower.arrow.location, 40
                )
                direction = self.get_antispin_antiradial_adjustment_direction(leader)
                if direction == UP:
                    if leader.end_loc == WEST:
                        adjustment += QPointF(-45, -20)
                    elif leader.end_loc == EAST:
                        adjustment += QPointF(45, -20)
                elif direction == DOWN:
                    if leader.end_loc == WEST:
                        adjustment += QPointF(-45, 20)
                    elif leader.end_loc == EAST:
                        adjustment += QPointF(45, 20)
                elif direction == LEFT:
                    if leader.end_loc == NORTH:
                        adjustment += QPointF(-20, -45)
                    elif leader.end_loc == SOUTH:
                        adjustment += QPointF(-20, 45)
                elif direction == RIGHT:
                    if leader.end_loc == NORTH:
                        adjustment += QPointF(20, -45)
                    elif leader.end_loc == SOUTH:
                        adjustment += QPointF(20, 45)
                self.arrow_positioner._apply_adjustment(leader.arrow, adjustment)

    def determine_leading_motion_for_T(
        self, red_start, red_end, blue_start, blue_end
    ) -> Literal["red", "blue"] | None:
        """Determines which motion is leading in the rotation sequence."""
        if red_start == blue_end:
            return "red"
        elif blue_start == red_end:
            return "blue"
        return None

    def _adjust_arrows_for_letter_U(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            leader = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == PRO
                else self.pictograph.motions[BLUE]
            )
            follower = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == ANTI
                else self.pictograph.motions[BLUE]
            )
            if follower.prop.is_antiradial():
                default_pos = self.arrow_positioner._get_default_position(
                    follower.arrow
                )
                adjustment = self.arrow_positioner.calculate_adjustment(
                    follower.arrow.location, DISTANCE + -45
                )
                new_pos = (
                    default_pos + adjustment - follower.arrow.boundingRect().center()
                )
                follower.arrow.setPos(new_pos)

            elif leader.prop.is_radial() and follower.prop.is_antiradial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    follower.arrow.location, 40
                )
                direction = self.get_antispin_antiradial_adjustment_direction(leader)
                if direction == UP:
                    if leader.end_loc == WEST:
                        adjustment += QPointF(-45, -20)
                    elif leader.end_loc == EAST:
                        adjustment += QPointF(45, -20)
                elif direction == DOWN:
                    if leader.end_loc == WEST:
                        adjustment += QPointF(-45, 20)
                    elif leader.end_loc == EAST:
                        adjustment += QPointF(45, 20)
                elif direction == LEFT:
                    if leader.end_loc == NORTH:
                        adjustment += QPointF(-20, -45)
                    elif leader.end_loc == SOUTH:
                        adjustment += QPointF(-20, 45)
                elif direction == RIGHT:
                    if leader.end_loc == NORTH:
                        adjustment += QPointF(20, -45)
                    elif leader.end_loc == SOUTH:
                        adjustment += QPointF(20, 45)
                self.arrow_positioner._apply_adjustment(leader.arrow, adjustment)

    def _adjust_arrows_for_letter_V(self, red_motion, blue_motion) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
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
                direction = self.get_antispin_antiradial_adjustment_direction(
                    anti_motion
                )
                if direction == UP:
                    adjustment += QPointF(0, -40)
                elif direction == DOWN:
                    adjustment += QPointF(0, 40)
                elif direction == LEFT:
                    adjustment += QPointF(-40, 0)
                elif direction == RIGHT:
                    adjustment += QPointF(40, 0)
                self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)

            elif anti_motion.prop.is_radial() and pro_motion.prop.is_antiradial():
                adjustment = self.arrow_positioner.calculate_adjustment(
                    pro_motion.arrow.location, 40
                )
                direction = self.get_antispin_antiradial_adjustment_direction(
                    anti_motion
                )
                if direction == UP:
                    if anti_motion.end_loc == WEST:
                        adjustment += QPointF(-45, -20)
                    elif anti_motion.end_loc == EAST:
                        adjustment += QPointF(45, -20)
                elif direction == DOWN:
                    if anti_motion.end_loc == WEST:
                        adjustment += QPointF(-45, 20)
                    elif anti_motion.end_loc == EAST:
                        adjustment += QPointF(45, 20)
                elif direction == LEFT:
                    if anti_motion.end_loc == NORTH:
                        adjustment += QPointF(-20, -45)
                    elif anti_motion.end_loc == SOUTH:
                        adjustment += QPointF(-20, -45)
                elif direction == RIGHT:
                    if anti_motion.end_loc == NORTH:
                        adjustment += QPointF(20, -45)
                    elif anti_motion.end_loc == SOUTH:
                        adjustment += QPointF(20, 45)
                self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)

    def get_antispin_antiradial_adjustment_direction(self, leader: "Motion") -> str:
        arrow_location = leader.arrow.location
        prop_location = leader.prop.location

        antiradial_mapping = {
            (NORTHEAST, EAST): DOWN,
            (NORTHEAST, NORTH): LEFT,
            (SOUTHEAST, SOUTH): LEFT,
            (SOUTHEAST, EAST): UP,
            (SOUTHWEST, WEST): UP,
            (SOUTHWEST, SOUTH): RIGHT,
            (NORTHWEST, NORTH): RIGHT,
            (NORTHWEST, WEST): DOWN,
        }

        radial_mapping = {
            (NORTHEAST, EAST): DOWN,
            (NORTHEAST, NORTH): LEFT,
            (SOUTHEAST, SOUTH): LEFT,
            (SOUTHEAST, EAST): UP,
            (SOUTHWEST, WEST): UP,
            (SOUTHWEST, SOUTH): RIGHT,
            (NORTHWEST, NORTH): RIGHT,
            (NORTHWEST, WEST): DOWN,
        }

        if leader.prop.is_antiradial():
            return antiradial_mapping.get((arrow_location, prop_location))
        else:
            return radial_mapping.get((arrow_location, prop_location))

    def _adjust_arrows_for_letter_X(
        self, red_motion: Motion, blue_motion: Motion
    ) -> None:
        # use the leader adjustment method to get the direction then apply the adjustment
        anti_motion = red_motion if red_motion.motion_type == ANTI else blue_motion
        if anti_motion.prop.is_antiradial():
            adjustment = self.arrow_positioner.calculate_adjustment(
                anti_motion.arrow.location, 30
            )
            direction = self.get_antispin_antiradial_adjustment_direction(anti_motion)
            if direction == UP:
                adjustment += QPointF(0, -40)
            elif direction == DOWN:
                adjustment += QPointF(0, 40)
            elif direction == LEFT:
                adjustment += QPointF(-40, 0)
            elif direction == RIGHT:
                adjustment += QPointF(40, 0)
            self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)

    def _adjust_arrows_for_letter_Z(
        self, red_motion: Motion, blue_motion: Motion
    ) -> None:
        if self._is_at_least_one_prop_antiradial(red_motion, blue_motion):
            anti_motion = (
                self.pictograph.motions[RED]
                if self.pictograph.motions[RED].motion_type == ANTI
                else self.pictograph.motions[BLUE]
            )
            adjustment = self.arrow_positioner.calculate_adjustment(
                anti_motion.arrow.location, 80
            )
            self.arrow_positioner._apply_adjustment(anti_motion.arrow, adjustment)
        elif red_motion.prop.orientation == OUT or blue_motion.prop.orientation == OUT:
            for arrow in self.pictograph.arrows.values():
                if arrow.motion.prop.orientation == OUT:
                    adjustment = self.arrow_positioner.calculate_adjustment(
                        arrow.location, 55
                    )
                    self.arrow_positioner._apply_adjustment(arrow, adjustment)

    # Helper functions
    def _are_both_props_radial(self, red_motion: Motion, blue_motion: Motion) -> bool:
        return (
            red_motion.prop.orientation in RadialOrientation
            and blue_motion.prop.orientation in RadialOrientation
        )

    def _is_at_least_one_prop_antiradial(
        self, red_motion: Motion, blue_motion: Motion
    ) -> bool:
        return (
            red_motion.prop.orientation in AntiradialOrientation
            or blue_motion.prop.orientation in AntiradialOrientation
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
