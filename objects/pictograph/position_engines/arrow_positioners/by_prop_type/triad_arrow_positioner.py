from typing import TYPE_CHECKING, List


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioners.base_arrow_positioner import (
        BaseArrowPositioner,
    )
from PyQt6.QtCore import QPointF
from objects.arrow import Arrow
from constants import ANTI, BLUE, IN, OUT, RED


class TriadArrowPositioner:
    def __init__(
        self, pictograph: "Pictograph", arrow_positioner: "BaseArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.arrow_positioner = arrow_positioner

    def _adjust_arrows_for_triads(self, current_letter):
        if current_letter == "I":
            self._adjust_triads_for_letter_I()
        elif current_letter == "H":
            self._adjust_triads_for_letter_H()
        elif current_letter == "Q":
            self._adjust_triads_for_letter_Q()
        elif current_letter == "R":
            self._adjust_triads_for_letter_R()
        elif current_letter == "Z":
            self._adjust_triads_for_letter_Z()
        elif current_letter == "K":
            self._adjust_triads_for_letter_K()
        elif current_letter == "L":
            self._adjust_triads_for_letter_L()

        else:
            for arrow in self.pictograph.arrows.values():
                if (
                    self.arrow_positioner._is_arrow_movable(arrow)
                    and arrow.motion.motion_type == ANTI
                ):
                    self._adjust_triad_anti_arrows()

    def _adjust_triads_for_letter_L(self):
        if (
            self.pictograph.arrows["red"].motion.end_ori == IN
            and self.pictograph.arrows["blue"].motion.end_ori == IN
        ):
            for arrow in self.pictograph.arrows.values():
                if arrow.motion.motion_type == ANTI:
                    if self.arrow_positioner._is_arrow_movable(arrow):
                        adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                            arrow.loc, 90
                        )
                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)

                else:
                    if self.arrow_positioner._is_arrow_movable(arrow):
                        adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                            arrow.loc, 40
                        )
                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)
        else:
            for arrow in self.pictograph.arrows.values():
                if arrow.motion.motion_type == ANTI:
                    if self.arrow_positioner._is_arrow_movable(arrow):
                        adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                            arrow.loc, 80
                        )
                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)

                else:
                    if self.arrow_positioner._is_arrow_movable(arrow):
                        adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                            arrow.loc, 40
                        )
                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)

    def _adjust_triads_for_letter_K(self):
        if (
            self.pictograph.arrows["red"].motion.end_ori == IN
            and self.pictograph.arrows["blue"].motion.end_ori == IN
        ):
            for arrow in self.pictograph.arrows.values():
                if self.arrow_positioner._is_arrow_movable(arrow):
                    adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                        arrow.loc, 90
                    )

                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)
        else:
            for arrow in self.pictograph.arrows.values():
                if self.arrow_positioner._is_arrow_movable(arrow):
                    adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                        arrow.loc, 80
                    )

                    self.arrow_positioner._apply_shift_adjustment(arrow, adjustment)

    def _adjust_triads_for_letter_Z(self):
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    arrow.loc, 80
                )
                adjusted_x = (
                    adjustment.x() - 10 if adjustment.x() < 0 else adjustment.x() + 10
                )
                adjusted_y = (
                    adjustment.y() - 10 if adjustment.y() < 0 else adjustment.y() + 10
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_shift_adjustment(
                    arrow, adjusted_adjustment
                )

    def _adjust_triads_for_letter_R(self):
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_R_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 55 if adjustment.x() < 0 else adjustment.x() + 55
                )
                adjusted_y = (
                    adjustment.y() - 55 if adjustment.y() < 0 else adjustment.y() + 55
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_shift_adjustment(
                    arrow, adjusted_adjustment
                )

    def _adjust_triads_for_letter_Q(self):
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_Q_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 55 if adjustment.x() < 0 else adjustment.x() + 55
                )
                adjusted_y = (
                    adjustment.y() - 55 if adjustment.y() < 0 else adjustment.y() + 55
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_shift_adjustment(
                    arrow, adjusted_adjustment
                )

    def _adjust_triad_anti_arrows(self):
        # Store arrows by color for easy access
        arrows_by_color = {
            arrow.color: arrow for arrow in self.pictograph.arrows.values()
        }

        red_arrow = arrows_by_color.get(RED)
        blue_arrow = arrows_by_color.get(BLUE)

        anti_arrows: List[Arrow] = []
        pro_arrows: List[Arrow] = []

        # Store arrows by motion type for easy access
        if red_arrow.motion.motion_type == ANTI:
            anti_arrows.append(red_arrow)
        else:
            pro_arrows.append(red_arrow)

        if blue_arrow.motion.motion_type == ANTI:
            anti_arrows.append(blue_arrow)
        else:
            pro_arrows.append(blue_arrow)

        # Check for the special condition
        for anti_arrow in anti_arrows:
            if anti_arrow.motion.end_ori == IN:
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    anti_arrow.loc, 85
                )
                self.arrow_positioner._apply_shift_adjustment(anti_arrow, adjustment)
            elif anti_arrow.motion.end_ori == OUT:
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    anti_arrow.loc, 85
                )
                self.arrow_positioner._apply_shift_adjustment(anti_arrow, adjustment)
            elif (
                anti_arrow.motion.end_ori == OUT and pro_arrows[0].motion.end_ori == IN
            ):
                adjustment = self.arrow_positioner._calculate_adjustment_tuple(
                    anti_arrow.loc, 85
                )
                self.arrow_positioner._apply_shift_adjustment(anti_arrow, adjustment)

    def _adjust_triads_for_letter_I(self):
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_I_adjustment(arrow)
                # if the orientation is IN for both props in the pictograph:
                motions_with_in_orientation = [
                    arrow.motion
                    for arrow in self.pictograph.arrows.values()
                    if arrow.motion.end_ori == IN
                ]
                if len(motions_with_in_orientation) == 2:
                    adjusted_x = (
                        adjustment.x() - 35
                        if adjustment.x() < 0
                        else adjustment.x() + 35
                    )
                    adjusted_y = (
                        adjustment.y() - 35
                        if adjustment.y() < 0
                        else adjustment.y() + 35
                    )
                    adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                    self.arrow_positioner._apply_shift_adjustment(
                        arrow, adjusted_adjustment
                    )
                else:
                    adjusted_x = (
                        adjustment.x() - 20
                        if adjustment.x() < 0
                        else adjustment.x() + 20
                    )
                    adjusted_y = (
                        adjustment.y() - 20
                        if adjustment.y() < 0
                        else adjustment.y() + 20
                    )
                    adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                    self.arrow_positioner._apply_shift_adjustment(
                        arrow, adjusted_adjustment
                    )

    def _adjust_triads_for_letter_H(self):
        for arrow in self.pictograph.arrows.values():
            if self.arrow_positioner._is_arrow_movable(arrow):
                adjustment = self.arrow_positioner._calculate_GH_adjustment(arrow)
                adjusted_x = (
                    adjustment.x() - 30 if adjustment.x() < 0 else adjustment.x() + 30
                )
                adjusted_y = (
                    adjustment.y() - 30 if adjustment.y() < 0 else adjustment.y() + 30
                )
                adjusted_adjustment = QPointF(adjusted_x, adjusted_y)
                self.arrow_positioner._apply_shift_adjustment(
                    arrow, adjusted_adjustment
                )
