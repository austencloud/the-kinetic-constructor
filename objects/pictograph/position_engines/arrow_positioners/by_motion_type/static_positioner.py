from ..base_arrow_positioner import (
    BaseArrowPositioner,
)
from constants import (
    RED,
    BLUE,
    PRO,
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
)
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Callable

from PyQt6.QtCore import QPointF


class StaticPositioner(BaseArrowPositioner):
    ### POSITIONING METHODS ###
    def _reposition_GH(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_GH_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_I(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_I_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)
            self._apply_adjustment(arrow.ghost, adjustment)

    def _reposition_P(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_P_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_Q(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_Q_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_R(self) -> None:
        for arrow in [
            self.pictograph.arrows[RED],
            self.pictograph.arrows[BLUE],
        ]:
            adjustment = self._calculate_R_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    ### ADJUSTMENT CALCULATIONS ###
    def _calculate_GH_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 105 if arrow.color == RED else 50
        return self.calculate_adjustment(arrow.loc, distance)

    def _calculate_I_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 110 if arrow.motion_type == PRO else 55
        return self.calculate_adjustment(arrow.loc, distance)

    def _calculate_P_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 90 if arrow.color == RED else 35
        return self.calculate_adjustment(arrow.loc, distance)

    def _calculate_Q_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_dict = {
            RED: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(70, -110),
                    SOUTHEAST: QPointF(110, 70),
                    SOUTHWEST: QPointF(-70, 110),
                    NORTHWEST: QPointF(-110, -70),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(110, -70),
                    SOUTHEAST: QPointF(70, 110),
                    SOUTHWEST: QPointF(-110, 70),
                    NORTHWEST: QPointF(-70, -110),
                },
            },
            BLUE: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
            },
        }
        color_adjustments = adjustment_dict.get(arrow.color, {})
        rotation_adjustments = color_adjustments.get(arrow.motion.prop_rot_dir, {})
        return rotation_adjustments.get(arrow.loc, QPointF(0, 0))

    def _calculate_R_adjustment(self, arrow: Arrow) -> QPointF:
        adjustment_dict = {
            PRO: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(75, -60),
                    SOUTHEAST: QPointF(60, 75),
                    SOUTHWEST: QPointF(-75, 60),
                    NORTHWEST: QPointF(-60, -75),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(60, -75),
                    SOUTHEAST: QPointF(75, 60),
                    SOUTHWEST: QPointF(-60, 75),
                    NORTHWEST: QPointF(-75, -60),
                },
            },
            ANTI: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(30, -30),
                    SOUTHEAST: QPointF(30, 30),
                    SOUTHWEST: QPointF(-30, 30),
                    NORTHWEST: QPointF(-30, -30),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(35, -25),
                    SOUTHEAST: QPointF(25, 35),
                    SOUTHWEST: QPointF(-35, 25),
                    NORTHWEST: QPointF(-25, -35),
                },
            },
        }
        motion_type_adjustments = adjustment_dict.get(arrow.motion_type, {})
        rotation_adjustments = motion_type_adjustments.get(
            arrow.motion.prop_rot_dir, {}
        )
        return rotation_adjustments.get(arrow.loc, QPointF(0, 0))
