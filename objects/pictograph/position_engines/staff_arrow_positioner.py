from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.pictograph.position_engines.arrow_positioner import ArrowPositioner
from constants.string_constants import ANTI, BLUE, IN, OUT, RED
from PyQt6.QtCore import QPointF
from objects.arrow.arrow import Arrow


class StaffArrowPositioner:
    def __init__(
        self, pictograph: "Pictograph", arrow_positioner: "ArrowPositioner"
    ) -> None:
        self.pictograph = pictograph
        self.arrow_positioner = arrow_positioner

    def _adjust_arrows_for_staffs(self, current_letter):
        if current_letter == "K":
            self._adjust_staffs_for_letter_K()
        elif current_letter == "L":
            self._adjust_staffs_for_letter_L()

    def _adjust_staffs_for_letter_K(self):
        if (
            (
                self.pictograph.arrows["red"].motion.end_orientation == OUT
                and self.pictograph.arrows["blue"].motion.end_orientation == OUT
            )
            or (
                self.pictograph.arrows["red"].motion.end_orientation == OUT
                and self.pictograph.arrows["blue"].motion.end_orientation == IN
            )
            or (
                self.pictograph.arrows["red"].motion.end_orientation == IN
                and self.pictograph.arrows["blue"].motion.end_orientation == OUT
            )
        ):
            for arrow in self.pictograph.arrows.values():
                if self.arrow_positioner._is_arrow_movable(arrow):
                    adjustment = self.arrow_positioner._calculate_adjustment(
                        arrow.location, 55
                    )
                self.arrow_positioner._apply_adjustment(arrow, adjustment)

    def _adjust_staffs_for_letter_L(self):
        if (
            (
                self.pictograph.arrows["red"].motion.end_orientation == OUT
                and self.pictograph.arrows["blue"].motion.end_orientation == OUT
            )
            or (
                self.pictograph.arrows["red"].motion.end_orientation == OUT
                and self.pictograph.arrows["blue"].motion.end_orientation == IN
            )
            or (
                self.pictograph.arrows["red"].motion.end_orientation == IN
                and self.pictograph.arrows["blue"].motion.end_orientation == OUT
            )
        ):
            for arrow in self.pictograph.arrows.values():
                if arrow.motion_type == ANTI:
                    if arrow.motion.end_orientation == OUT:
                        adjustment = self.arrow_positioner._calculate_adjustment(
                            arrow.location, 55
                        )
                        self.arrow_positioner._apply_adjustment(arrow, adjustment)
