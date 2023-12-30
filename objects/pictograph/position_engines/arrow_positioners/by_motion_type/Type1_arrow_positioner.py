from objects.pictograph.position_engines.arrow_positioners.base_arrow_positioner import (
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
from PyQt6.QtCore import QPointF


class Type1ArrowPositioner(BaseArrowPositioner):
    ### POSITIONING METHODS ###
    def _reposition_G_H(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_G_H_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_I(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_I_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)
            self._apply_adjustment(arrow.ghost, adjustment)

    def _reposition_P(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_P_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_Q(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_Q_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    def _reposition_R(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_R_adjustment(arrow)
            self._apply_adjustment(arrow, adjustment)

    ### ADJUSTMENT CALCULATIONS ###
    def _calculate_G_H_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 105 if arrow.color == RED else 50
        return self.calculate_adjustment(arrow.location, distance)

    def _calculate_I_adjustment(self, arrow: Arrow) -> QPointF:
        distance = 110 if arrow.motion_type == PRO else 55
        return self.calculate_adjustment(arrow.location, distance)

    def _calculate_P_adjustment(self, arrow: Arrow) -> QPointF:
        blue_adjustments = {
            NORTHEAST: QPointF(35, -35),
            SOUTHEAST: QPointF(35, 35),
            SOUTHWEST: QPointF(-35, 35),
            NORTHWEST: QPointF(-35, -35),
        }

        red_ccw_adjustments = {
            NORTHEAST: QPointF(70, -110),
            SOUTHEAST: QPointF(110, 70),
            SOUTHWEST: QPointF(-70, 110),
            NORTHWEST: QPointF(-110, -70),
        }

        red_cw_adjustments = {
            NORTHEAST: QPointF(110, -70),
            SOUTHEAST: QPointF(70, 110),
            SOUTHWEST: QPointF(-110, 70),
            NORTHWEST: QPointF(-70, -110),
        }

        adjustments = {
            RED: {
                CLOCKWISE: red_cw_adjustments,
                COUNTER_CLOCKWISE: red_ccw_adjustments,
            },
            BLUE: {
                CLOCKWISE: blue_adjustments,
                COUNTER_CLOCKWISE: blue_adjustments,
            },
        }

        color_adjustments = adjustments.get(arrow.color, {})
        rotation_adjustments = color_adjustments.get(arrow.motion.prop_rot_dir, {})
        return rotation_adjustments.get(arrow.location, QPointF(0, 0))

    def _calculate_Q_adjustment(self, arrow: Arrow) -> QPointF:
        blue_adjustments = {
            NORTHEAST: QPointF(35, -35),
            SOUTHEAST: QPointF(35, 35),
            SOUTHWEST: QPointF(-35, 35),
            NORTHWEST: QPointF(-35, -35),
        }

        red_cw_adjustments = {
            NORTHEAST: QPointF(70, -110),
            SOUTHEAST: QPointF(110, 70),
            SOUTHWEST: QPointF(-70, 110),
            NORTHWEST: QPointF(-110, -70),
        }

        red_ccw_adjustments = {
            NORTHEAST: QPointF(110, -70),
            SOUTHEAST: QPointF(70, 110),
            SOUTHWEST: QPointF(-110, 70),
            NORTHWEST: QPointF(-70, -110),
        }

        adjustments = {
            RED: {
                CLOCKWISE: red_cw_adjustments,
                COUNTER_CLOCKWISE: red_ccw_adjustments,
            },
            BLUE: {
                CLOCKWISE: blue_adjustments,
                COUNTER_CLOCKWISE: blue_adjustments,
            },
        }

        color_adjustments = adjustments.get(arrow.color, {})
        rotation_adjustments = color_adjustments.get(arrow.motion.prop_rot_dir, {})
        return rotation_adjustments.get(arrow.location, QPointF(0, 0))

    def _calculate_R_adjustment(self, arrow: Arrow) -> QPointF:
        pro_cw_adjustments = {
            NORTHEAST: QPointF(75, -60),
            SOUTHEAST: QPointF(60, 75),
            SOUTHWEST: QPointF(-75, 60),
            NORTHWEST: QPointF(-60, -75),
        }
        pro_ccw_adjustments = {
            NORTHEAST: QPointF(60, -75),
            SOUTHEAST: QPointF(75, 60),
            SOUTHWEST: QPointF(-60, 75),
            NORTHWEST: QPointF(-75, -60),
        }

        anti_cw_adjustments = {
            NORTHEAST: QPointF(30, -30),
            SOUTHEAST: QPointF(30, 30),
            SOUTHWEST: QPointF(-30, 30),
            NORTHWEST: QPointF(-30, -30),
        }
        anti_ccw_adjustments = {
            NORTHEAST: QPointF(35, -25),
            SOUTHEAST: QPointF(25, 35),
            SOUTHWEST: QPointF(-35, 25),
            NORTHWEST: QPointF(-25, -35),
        }

        adjustments = {
            PRO: {
                CLOCKWISE: pro_cw_adjustments,
                COUNTER_CLOCKWISE: pro_ccw_adjustments,
            },
            ANTI: {
                CLOCKWISE: anti_cw_adjustments,
                COUNTER_CLOCKWISE: anti_ccw_adjustments,
            },
        }

        motion_type_adjustments = adjustments.get(arrow.motion_type, {})
        rotation_adjustments = motion_type_adjustments.get(
            arrow.motion.prop_rot_dir, {}
        )
        return rotation_adjustments.get(arrow.location, QPointF(0, 0))
