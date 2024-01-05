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
from objects.arrow import Arrow
from PyQt6.QtCore import QPointF


class Type1ArrowPositioner(BaseArrowPositioner):
    ### POSITIONING METHODS ###
    def _reposition_E(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_E_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    def _reposition_G(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_G_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    def _reposition_H(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_H_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    def _reposition_I(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_I_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)
            self._apply_shift_adjustment(arrow.ghost, adjustment)

    def _reposition_P(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_P_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    def _reposition_Q(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_Q_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    def _reposition_R(self) -> None:
        for arrow in self.arrows:
            adjustment = self._calculate_R_adjustment(arrow)
            self._apply_shift_adjustment(arrow, adjustment)

    ### ADJUSTMENT CALCULATIONS ###

    def _calculate_E_adjustment(self, arrow: Arrow) -> QPointF:
        # Define the adjustments as a nested dictionary with keys representing
        # the 'turns' and 'prop_rot_dir' of the arrow for the special case of 0.5 and 2.5 turns
        adjustments = {
            0: {
                CLOCKWISE: {  # Since both directions are the same, we just need one key
                    NORTHEAST: QPointF(35, -35),
                    SOUTHEAST: QPointF(35, 35),
                    SOUTHWEST: QPointF(-35, 35),
                    NORTHWEST: QPointF(-35, -35),
                }
            },
            0.5: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(-60, 115),
                    SOUTHEAST: QPointF(-115, -60),
                    SOUTHWEST: QPointF(60, -115),
                    NORTHWEST: QPointF(115, 60),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(-115, 60),
                    SOUTHEAST: QPointF(-60, -115),
                    SOUTHWEST: QPointF(115, -60),
                    NORTHWEST: QPointF(60, 115),
                },
            },
            1.5: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(-70, 5),
                    SOUTHEAST: QPointF(-5, -70),
                    SOUTHWEST: QPointF(70, -5),
                    NORTHWEST: QPointF(5, 70),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(-5, 70),
                    SOUTHEAST: QPointF(-70, -5),
                    SOUTHWEST: QPointF(5, -70),
                    NORTHWEST: QPointF(70, 5),
                },
            },
            2.5: {
                CLOCKWISE: {
                    NORTHEAST: QPointF(-55, 80),
                    SOUTHEAST: QPointF(-80, -55),
                    SOUTHWEST: QPointF(55, -80),
                    NORTHWEST: QPointF(80, 55),
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: QPointF(-80, 55),
                    SOUTHEAST: QPointF(-55, -80),
                    SOUTHWEST: QPointF(80, -55),
                    NORTHWEST: QPointF(55, 80),
                },
            },
        }

        # For turns 0, 1, 2, 3, the adjustments are the same for all cases
        if arrow.turns in [0, 1, 2, 3]:
            return adjustments[0][CLOCKWISE].get(arrow.loc, QPointF(0, 0))

        # For the special cases of 0.5 and 2.5 turns, the adjustments depend on the prop_rot_dir
        direction_adjustments = adjustments.get(arrow.turns, {})
        return direction_adjustments.get(arrow.motion.prop_rot_dir, {}).get(
            arrow.loc, QPointF(0, 0)
        )

    def _calculate_G_adjustment(self, arrow: Arrow) -> QPointF:
        adjustments = {
            0: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(80, -100),
                        SOUTHEAST: QPointF(100, 80),
                        SOUTHWEST: QPointF(-80, 100),
                        NORTHWEST: QPointF(-100, -80),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(100, -80),
                        SOUTHEAST: QPointF(80, 100),
                        SOUTHWEST: QPointF(-100, 80),
                        NORTHWEST: QPointF(-80, -100),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(35, -35),
                        SOUTHEAST: QPointF(35, 35),
                        SOUTHWEST: QPointF(-35, 35),
                        NORTHWEST: QPointF(-35, -35),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(35, -35),
                        SOUTHEAST: QPointF(35, 35),
                        SOUTHWEST: QPointF(-35, 35),
                        NORTHWEST: QPointF(-35, -35),
                    },
                },
            },
            0.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(45, 100),
                        SOUTHEAST: QPointF(-100, 45),
                        SOUTHWEST: QPointF(-45, -100),
                        NORTHWEST: QPointF(100, -45),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-100, -45),
                        SOUTHEAST: QPointF(45, -100),
                        SOUTHWEST: QPointF(100, 45),
                        NORTHWEST: QPointF(-45, 100),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(10, 30),
                        SOUTHEAST: QPointF(-30, 10),
                        SOUTHWEST: QPointF(-10, -30),
                        NORTHWEST: QPointF(30, -10),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-30, -10),
                        SOUTHEAST: QPointF(10, -30),
                        SOUTHWEST: QPointF(30, 10),
                        NORTHWEST: QPointF(-10, 30),
                    },
                },
            },
            1: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(40, -25),
                        SOUTHEAST: QPointF(25, 40),
                        SOUTHWEST: QPointF(-40, 25),
                        NORTHWEST: QPointF(-25, -40),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(25, -40),
                        SOUTHEAST: QPointF(40, 25),
                        SOUTHWEST: QPointF(-25, 40),
                        NORTHWEST: QPointF(-40, -25),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-45, -35),
                        SOUTHEAST: QPointF(35, -45),
                        SOUTHWEST: QPointF(45, 35),
                        NORTHWEST: QPointF(-35, 45),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(35, 45),
                        SOUTHEAST: QPointF(-45, 35),
                        SOUTHWEST: QPointF(-35, -45),
                        NORTHWEST: QPointF(45, -35),
                    },
                },
            },
            1.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(1, 35),
                        SOUTHEAST: QPointF(-35, -1),
                        SOUTHWEST: QPointF(1, -35),
                        NORTHWEST: QPointF(35, 1),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-35, -1),
                        SOUTHEAST: QPointF(-1, -35),
                        SOUTHWEST: QPointF(35, -1),
                        NORTHWEST: QPointF(1, 35),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-30, -29),
                        SOUTHEAST: QPointF(29, -30),
                        SOUTHWEST: QPointF(30, 29),
                        NORTHWEST: QPointF(-29, 30),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(29, 30),
                        SOUTHEAST: QPointF(-30, 29),
                        SOUTHWEST: QPointF(-29, -30),
                        NORTHWEST: QPointF(30, -29),
                    },
                },
            },
            2: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(95, -105),
                        SOUTHEAST: QPointF(105, 95),
                        SOUTHWEST: QPointF(-95, 105),
                        NORTHWEST: QPointF(-105, -95),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(105, -95),
                        SOUTHEAST: QPointF(95, 105),
                        SOUTHWEST: QPointF(-105, 95),
                        NORTHWEST: QPointF(-95, -105),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(40, -45),
                        SOUTHEAST: QPointF(45, 40),
                        SOUTHWEST: QPointF(-40, 45),
                        NORTHWEST: QPointF(-45, -40),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(45, -40),
                        SOUTHEAST: QPointF(40, 45),
                        SOUTHWEST: QPointF(-45, 40),
                        NORTHWEST: QPointF(-40, -45),
                    },
                },
            },
            2.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(5, -35),
                        SOUTHEAST: QPointF(35, 5),
                        SOUTHWEST: QPointF(-5, 35),
                        NORTHWEST: QPointF(-35, -5),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(35, -5),
                        SOUTHEAST: QPointF(5, 35),
                        SOUTHWEST: QPointF(-35, 5),
                        NORTHWEST: QPointF(-5, -35),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(30, 65),
                        SOUTHEAST: QPointF(-65, 30),
                        SOUTHWEST: QPointF(-30, -65),
                        NORTHWEST: QPointF(65, -30),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-65, -30),
                        SOUTHEAST: QPointF(30, -65),
                        SOUTHWEST: QPointF(65, 30),
                        NORTHWEST: QPointF(-30, 65),
                    },
                },
            },
            3: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(30, -25),
                        SOUTHEAST: QPointF(25, 30),
                        SOUTHWEST: QPointF(-30, 25),
                        NORTHWEST: QPointF(-25, -30),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(25, -30),
                        SOUTHEAST: QPointF(30, 25),
                        SOUTHWEST: QPointF(-25, 30),
                        NORTHWEST: QPointF(-30, -25),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-45, -35),
                        SOUTHEAST: QPointF(35, -45),
                        SOUTHWEST: QPointF(45, 35),
                        NORTHWEST: QPointF(-35, 45),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(35, 45),
                        SOUTHEAST: QPointF(-45, 35),
                        SOUTHWEST: QPointF(-35, -45),
                        NORTHWEST: QPointF(45, -35),
                    },
                },
            },
        }
        turn_adjustments = adjustments.get(arrow.turns, {})
        color_adjustments = turn_adjustments.get(arrow.color, {})
        direction_adjustments = color_adjustments.get(arrow.motion.prop_rot_dir, {})
        return direction_adjustments.get(arrow.loc, QPointF(0, 0))

    def _calculate_H_adjustment(self, arrow: Arrow) -> QPointF:
        adjustments = {
            0: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(125, -65),
                        SOUTHEAST: QPointF(65, 125),
                        SOUTHWEST: QPointF(-125, 65),
                        NORTHWEST: QPointF(-65, -125),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(65, -125),
                        SOUTHEAST: QPointF(125, 65),
                        SOUTHWEST: QPointF(-65, 125),
                        NORTHWEST: QPointF(-125, -65),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(55, -15),
                        SOUTHEAST: QPointF(15, 55),
                        SOUTHWEST: QPointF(-55, 15),
                        NORTHWEST: QPointF(-15, -55),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(15, -55),
                        SOUTHEAST: QPointF(55, 15),
                        SOUTHWEST: QPointF(-15, 55),
                        NORTHWEST: QPointF(-55, -15),
                    },
                },
            },
            0.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-105, 155),
                        SOUTHEAST: QPointF(-155, -105),
                        SOUTHWEST: QPointF(105, -155),
                        NORTHWEST: QPointF(155, 105),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-155, 105),
                        SOUTHEAST: QPointF(-105, -155),
                        SOUTHWEST: QPointF(155, -105),
                        NORTHWEST: QPointF(105, 155),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-55, 115),
                        SOUTHEAST: QPointF(-115, -55),
                        SOUTHWEST: QPointF(55, -115),
                        NORTHWEST: QPointF(115, 55),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-115, 55),
                        SOUTHEAST: QPointF(-55, -115),
                        SOUTHWEST: QPointF(115, -55),
                        NORTHWEST: QPointF(55, 115),
                    },
                },
            },
            1: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(125, -65),
                        SOUTHEAST: QPointF(65, 125),
                        SOUTHWEST: QPointF(-125, 65),
                        NORTHWEST: QPointF(-65, -125),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(65, -125),
                        SOUTHEAST: QPointF(125, 65),
                        SOUTHWEST: QPointF(-65, 125),
                        NORTHWEST: QPointF(-125, -65),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(55, -15),
                        SOUTHEAST: QPointF(15, 55),
                        SOUTHWEST: QPointF(-55, 15),
                        NORTHWEST: QPointF(-15, -55),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(15, -55),
                        SOUTHEAST: QPointF(55, 15),
                        SOUTHWEST: QPointF(-15, 55),
                        NORTHWEST: QPointF(-55, -15),
                    },
                },
            },
            1.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-80, -1),
                        SOUTHEAST: QPointF(1, -80),
                        SOUTHWEST: QPointF(80, 1),
                        NORTHWEST: QPointF(-1, 80),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(1, 80),
                        SOUTHEAST: QPointF(-80, 1),
                        SOUTHWEST: QPointF(-1, -80),
                        NORTHWEST: QPointF(80, -1),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-30, -35),
                        SOUTHEAST: QPointF(35, -30),
                        SOUTHWEST: QPointF(30, 35),
                        NORTHWEST: QPointF(-35, 30),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(35, 30),
                        SOUTHEAST: QPointF(-30, 35),
                        SOUTHWEST: QPointF(-35, -30),
                        NORTHWEST: QPointF(30, -35),
                    },
                },
            },
            2: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(125, -65),
                        SOUTHEAST: QPointF(65, 125),
                        SOUTHWEST: QPointF(-125, 65),
                        NORTHWEST: QPointF(-65, -125),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(65, -125),
                        SOUTHEAST: QPointF(125, 65),
                        SOUTHWEST: QPointF(-65, 125),
                        NORTHWEST: QPointF(-125, -65),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(60, -20),
                        SOUTHEAST: QPointF(20, 60),
                        SOUTHWEST: QPointF(-60, 20),
                        NORTHWEST: QPointF(-20, -60),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(20, -60),
                        SOUTHEAST: QPointF(60, 20),
                        SOUTHWEST: QPointF(-20, 60),
                        NORTHWEST: QPointF(-60, -20),
                    },
                },
            },
            2.5: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-105, 155),
                        SOUTHEAST: QPointF(-155, -105),
                        SOUTHWEST: QPointF(105, -155),
                        NORTHWEST: QPointF(155, 105),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-155, 105),
                        SOUTHEAST: QPointF(-105, -155),
                        SOUTHWEST: QPointF(155, -105),
                        NORTHWEST: QPointF(105, 155),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(-60, 105),
                        SOUTHEAST: QPointF(-105, -60),
                        SOUTHWEST: QPointF(60, -105),
                        NORTHWEST: QPointF(105, 60),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(-105, 60),
                        SOUTHEAST: QPointF(-60, -105),
                        SOUTHWEST: QPointF(105, -60),
                        NORTHWEST: QPointF(60, 105),
                    },
                },
            },
            3: {
                RED: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(125, -65),
                        SOUTHEAST: QPointF(65, 125),
                        SOUTHWEST: QPointF(-125, 65),
                        NORTHWEST: QPointF(-65, -125),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(65, -125),
                        SOUTHEAST: QPointF(125, 65),
                        SOUTHWEST: QPointF(-65, 125),
                        NORTHWEST: QPointF(-125, -65),
                    },
                },
                BLUE: {
                    CLOCKWISE: {
                        NORTHEAST: QPointF(60, -20),
                        SOUTHEAST: QPointF(20, 60),
                        SOUTHWEST: QPointF(-60, 20),
                        NORTHWEST: QPointF(-20, -60),
                    },
                    COUNTER_CLOCKWISE: {
                        NORTHEAST: QPointF(20, -60),
                        SOUTHEAST: QPointF(60, 20),
                        SOUTHWEST: QPointF(-20, 60),
                        NORTHWEST: QPointF(-60, -20),
                    },
                },
            },
        }
        turn_adjustments = adjustments.get(arrow.turns, {})
        color_adjustments = turn_adjustments.get(arrow.color, {})
        direction_adjustments = color_adjustments.get(arrow.motion.prop_rot_dir, {})
        return direction_adjustments.get(arrow.loc, QPointF(0, 0))

    def _calculate_I_adjustment(self, arrow: Arrow) -> QPointF:
        pro_arrow = (
            arrow.scene.arrows[RED]
            if arrow.scene.arrows[RED].motion_type == PRO
            else arrow.scene.arrows[BLUE]
        )
        anti_arrow = (
            arrow.scene.arrows[RED]
            if arrow.scene.arrows[RED].motion_type == ANTI
            else arrow.scene.arrows[BLUE]
        )
        if pro_arrow.turns == anti_arrow.turns:
            adjustments = {
                0: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(75, -85),
                            SOUTHEAST: QPointF(85, 75),
                            SOUTHWEST: QPointF(-75, 85),
                            NORTHWEST: QPointF(-85, -75),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(85, -75),
                            SOUTHEAST: QPointF(75, 85),
                            SOUTHWEST: QPointF(-85, 75),
                            NORTHWEST: QPointF(-75, -85),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(50, -25),
                            SOUTHEAST: QPointF(25, 50),
                            SOUTHWEST: QPointF(-50, 25),
                            NORTHWEST: QPointF(-25, -50),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(25, -50),
                            SOUTHEAST: QPointF(50, 25),
                            SOUTHWEST: QPointF(-25, 50),
                            NORTHWEST: QPointF(-50, -25),
                        },
                    },
                },
                0.5: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(5, 40),
                            SOUTHEAST: QPointF(-40, 5),
                            SOUTHWEST: QPointF(-5, -40),
                            NORTHWEST: QPointF(40, -5),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(-40, -5),
                            SOUTHEAST: QPointF(5, -40),
                            SOUTHWEST: QPointF(40, 5),
                            NORTHWEST: QPointF(-5, 40),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-60, 115),
                            SOUTHEAST: QPointF(-115, -60),
                            SOUTHWEST: QPointF(60, -115),
                            NORTHWEST: QPointF(115, 60),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(-115, 60),
                            SOUTHEAST: QPointF(-60, -115),
                            SOUTHWEST: QPointF(115, -60),
                            NORTHWEST: QPointF(60, 115),
                        },
                    },
                },
                1: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(5, -50),
                            SOUTHEAST: QPointF(50, 5),
                            SOUTHWEST: QPointF(-5, 50),
                            NORTHWEST: QPointF(-50, -5),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(50, -5),
                            SOUTHEAST: QPointF(5, 50),
                            SOUTHWEST: QPointF(-50, 5),
                            NORTHWEST: QPointF(-5, -50),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(55, -15),
                            SOUTHEAST: QPointF(15, 55),
                            SOUTHWEST: QPointF(-55, 15),
                            NORTHWEST: QPointF(-15, -55),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(15, -55),
                            SOUTHEAST: QPointF(55, 15),
                            SOUTHWEST: QPointF(-15, 55),
                            NORTHWEST: QPointF(-55, -15),
                        },
                    },
                },
                1.5: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-30, 25),
                            SOUTHEAST: QPointF(-25, -30),
                            SOUTHWEST: QPointF(30, -25),
                            NORTHWEST: QPointF(25, 30),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(-25, 30),
                            SOUTHEAST: QPointF(-30, -25),
                            SOUTHWEST: QPointF(25, -30),
                            NORTHWEST: QPointF(30, 25),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-50, -45),
                            SOUTHEAST: QPointF(45, -50),
                            SOUTHWEST: QPointF(50, 45),
                            NORTHWEST: QPointF(-45, 50),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(45, 50),
                            SOUTHEAST: QPointF(-50, 45),
                            SOUTHWEST: QPointF(-45, -50),
                            NORTHWEST: QPointF(50, -45),
                        },
                    },
                },
                2: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(65, -100),
                            SOUTHEAST: QPointF(100, 65),
                            SOUTHWEST: QPointF(-65, 100),
                            NORTHWEST: QPointF(-100, -65),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(100, -65),
                            SOUTHEAST: QPointF(65, 100),
                            SOUTHWEST: QPointF(-100, 65),
                            NORTHWEST: QPointF(-65, -100),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(50, -25),
                            SOUTHEAST: QPointF(25, 50),
                            SOUTHWEST: QPointF(-50, 25),
                            NORTHWEST: QPointF(-25, -50),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(25, -50),
                            SOUTHEAST: QPointF(50, 25),
                            SOUTHWEST: QPointF(-25, 50),
                            NORTHWEST: QPointF(-50, -25),
                        },
                    },
                },
                2.5: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-105, 155),
                            SOUTHEAST: QPointF(-155, -105),
                            SOUTHWEST: QPointF(105, -155),
                            NORTHWEST: QPointF(155, 105),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(-155, 105),
                            SOUTHEAST: QPointF(-105, -155),
                            SOUTHWEST: QPointF(155, -105),
                            NORTHWEST: QPointF(105, 155),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-60, 105),
                            SOUTHEAST: QPointF(-105, -60),
                            SOUTHWEST: QPointF(60, -105),
                            NORTHWEST: QPointF(105, 60),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(-105, 60),
                            SOUTHEAST: QPointF(-60, -105),
                            SOUTHWEST: QPointF(105, -60),
                            NORTHWEST: QPointF(60, 105),
                        },
                    },
                },
                3: {
                    PRO: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(-45, -30),
                            SOUTHEAST: QPointF(30, -45),
                            SOUTHWEST: QPointF(45, 30),
                            NORTHWEST: QPointF(-30, 45),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(30, 45),
                            SOUTHEAST: QPointF(-45, 30),
                            SOUTHWEST: QPointF(-30, -45),
                            NORTHWEST: QPointF(45, -30),
                        },
                    },
                    ANTI: {
                        CLOCKWISE: {
                            NORTHEAST: QPointF(80, -75),
                            SOUTHEAST: QPointF(75, 80),
                            SOUTHWEST: QPointF(-80, 75),
                            NORTHWEST: QPointF(-75, -80),
                        },
                        COUNTER_CLOCKWISE: {
                            NORTHEAST: QPointF(75, -80),
                            SOUTHEAST: QPointF(80, 75),
                            SOUTHWEST: QPointF(-75, 80),
                            NORTHWEST: QPointF(-80, -75),
                        },
                    },
                },
            }
            turn_adjustments = adjustments.get(arrow.turns, {})
            motion_type_adjustments = turn_adjustments.get(arrow.motion_type, {})
            direction_adjustments = motion_type_adjustments.get(
                arrow.motion.prop_rot_dir, {}
            )

            return direction_adjustments.get(arrow.loc, QPointF(0, 0))
        elif pro_arrow.turns != anti_arrow.turns:
            if pro_arrow.turns == 0:
                if anti_arrow.turns == 0.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(50, -35),
                                SOUTHEAST: QPointF(35, 50),
                                SOUTHWEST: QPointF(-50, 35),
                                NORTHWEST: QPointF(-35, -50),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(35, -50),
                                SOUTHEAST: QPointF(50, 35),
                                SOUTHWEST: QPointF(-35, 50),
                                NORTHWEST: QPointF(-50, -35),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-110, 115),
                                SOUTHEAST: QPointF(-115, -110),
                                SOUTHWEST: QPointF(110, -115),
                                NORTHWEST: QPointF(115, 110),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-115, 110),
                                SOUTHEAST: QPointF(-110, -115),
                                SOUTHWEST: QPointF(115, -110),
                                NORTHWEST: QPointF(110, 115),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 1:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -85),
                                SOUTHEAST: QPointF(85, 75),
                                SOUTHWEST: QPointF(-75, 85),
                                NORTHWEST: QPointF(-85, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(85, -75),
                                SOUTHEAST: QPointF(75, 85),
                                SOUTHWEST: QPointF(-85, 75),
                                NORTHWEST: QPointF(-75, -85),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(50, -25),
                                SOUTHEAST: QPointF(25, 50),
                                SOUTHWEST: QPointF(-50, 25),
                                NORTHWEST: QPointF(-25, -50),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(25, -50),
                                SOUTHEAST: QPointF(50, 25),
                                SOUTHWEST: QPointF(-25, 50),
                                NORTHWEST: QPointF(-50, -25),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 1.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -80),
                                SOUTHEAST: QPointF(80, 75),
                                SOUTHWEST: QPointF(-75, 80),
                                NORTHWEST: QPointF(-80, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(80, -75),
                                SOUTHEAST: QPointF(75, 80),
                                SOUTHWEST: QPointF(-80, 75),
                                NORTHWEST: QPointF(-75, -80),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-65, -30),
                                SOUTHEAST: QPointF(30, -65),
                                SOUTHWEST: QPointF(65, 30),
                                NORTHWEST: QPointF(-30, 65),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(30, 65),
                                SOUTHEAST: QPointF(-65, 30),
                                SOUTHWEST: QPointF(-30, -65),
                                NORTHWEST: QPointF(65, -30),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 2:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -85),
                                SOUTHEAST: QPointF(85, 75),
                                SOUTHWEST: QPointF(-75, 85),
                                NORTHWEST: QPointF(-85, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(85, -75),
                                SOUTHEAST: QPointF(75, 85),
                                SOUTHWEST: QPointF(-85, 75),
                                NORTHWEST: QPointF(-75, -85),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(50, -25),
                                SOUTHEAST: QPointF(25, 50),
                                SOUTHWEST: QPointF(-50, 25),
                                NORTHWEST: QPointF(-25, -50),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(25, -50),
                                SOUTHEAST: QPointF(50, 25),
                                SOUTHWEST: QPointF(-25, 50),
                                NORTHWEST: QPointF(-50, -25),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 2.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(50, -35),
                                SOUTHEAST: QPointF(35, 50),
                                SOUTHWEST: QPointF(-50, 35),
                                NORTHWEST: QPointF(-35, -50),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(35, -50),
                                SOUTHEAST: QPointF(50, 35),
                                SOUTHWEST: QPointF(-35, 50),
                                NORTHWEST: QPointF(-50, -35),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-90, 110),
                                SOUTHEAST: QPointF(-110, -90),
                                SOUTHWEST: QPointF(90, -110),
                                NORTHWEST: QPointF(110, 90),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-110, 90),
                                SOUTHEAST: QPointF(-90, -110),
                                SOUTHWEST: QPointF(110, -90),
                                NORTHWEST: QPointF(90, 110),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 3:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -85),
                                SOUTHEAST: QPointF(85, 75),
                                SOUTHWEST: QPointF(-75, 85),
                                NORTHWEST: QPointF(-85, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(85, -75),
                                SOUTHEAST: QPointF(75, 85),
                                SOUTHWEST: QPointF(-85, 75),
                                NORTHWEST: QPointF(-75, -85),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(50, -25),
                                SOUTHEAST: QPointF(25, 50),
                                SOUTHWEST: QPointF(-50, 25),
                                NORTHWEST: QPointF(-25, -50),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(25, -50),
                                SOUTHEAST: QPointF(50, 25),
                                SOUTHWEST: QPointF(-25, 50),
                                NORTHWEST: QPointF(-50, -25),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
            elif pro_arrow.turns == 0.5:
                if anti_arrow.turns == 0:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-15, 55),
                                SOUTHEAST: QPointF(-55, -15),
                                SOUTHWEST: QPointF(15, -55),
                                NORTHWEST: QPointF(55, 15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-55, 15),
                                SOUTHEAST: QPointF(-15, -55),
                                SOUTHWEST: QPointF(55, -15),
                                NORTHWEST: QPointF(15, 55),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -70),
                                SOUTHEAST: QPointF(70, 75),
                                SOUTHWEST: QPointF(-75, 70),
                                NORTHWEST: QPointF(-70, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -75),
                                SOUTHEAST: QPointF(75, 70),
                                SOUTHWEST: QPointF(-70, 75),
                                NORTHWEST: QPointF(-75, -70),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 1:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-15, 55),
                                SOUTHEAST: QPointF(-55, -15),
                                SOUTHWEST: QPointF(15, -55),
                                NORTHWEST: QPointF(55, 15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-55, 15),
                                SOUTHEAST: QPointF(-15, -55),
                                SOUTHWEST: QPointF(55, -15),
                                NORTHWEST: QPointF(15, 55),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(75, -70),
                                SOUTHEAST: QPointF(70, 75),
                                SOUTHWEST: QPointF(-75, 70),
                                NORTHWEST: QPointF(-70, -75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -75),
                                SOUTHEAST: QPointF(75, 70),
                                SOUTHWEST: QPointF(-70, 75),
                                NORTHWEST: QPointF(-75, -70),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 1.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(30, 90),
                                SOUTHEAST: QPointF(-90, 30),
                                SOUTHWEST: QPointF(-30, -90),
                                NORTHWEST: QPointF(90, -30),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-90, -30),
                                SOUTHEAST: QPointF(30, -90),
                                SOUTHWEST: QPointF(90, 30),
                                NORTHWEST: QPointF(-30, 90),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-15, -35),
                                SOUTHEAST: QPointF(35, -15),
                                SOUTHWEST: QPointF(15, 35),
                                NORTHWEST: QPointF(-35, 15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(35, 15),
                                SOUTHEAST: QPointF(-15, 35),
                                SOUTHWEST: QPointF(-35, -15),
                                NORTHWEST: QPointF(15, -35),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))

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
        return rotation_adjustments.get(arrow.loc, QPointF(0, 0))

    def _calculate_Q_adjustment(self, arrow: Arrow) -> QPointF:
        if arrow.turns in [0, 1, 2, 3]:
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
            return rotation_adjustments.get(arrow.loc, QPointF(0, 0))

        elif arrow.turns == 0.5:
            if arrow.motion.prop_rot_dir == CLOCKWISE:
                adjustments = {
                    NORTHEAST: QPointF(-60, 95),
                    SOUTHEAST: QPointF(-95, -60),
                    SOUTHWEST: QPointF(60, -95),
                    NORTHWEST: QPointF(95, 60),
                }
            elif arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                adjustments = {
                    NORTHEAST: QPointF(-95, 60),
                    SOUTHEAST: QPointF(-60, -95),
                    SOUTHWEST: QPointF(95, -60),
                    NORTHWEST: QPointF(60, 95),
                }

            return adjustments.get(arrow.loc, QPointF(0, 0))

        elif arrow.turns == 1.5:
            return QPointF(0, 0)

        elif arrow.turns == 2.5:
            if arrow.motion.prop_rot_dir == CLOCKWISE:
                adjustments = {
                    NORTHEAST: QPointF(-95, 94),
                    SOUTHEAST: QPointF(-94, -95),
                    SOUTHWEST: QPointF(95, -94),
                    NORTHWEST: QPointF(94, 95),
                }
            elif arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
                adjustments = {
                    NORTHEAST: QPointF(-94, 95),
                    SOUTHEAST: QPointF(-95, -94),
                    SOUTHWEST: QPointF(94, -95),
                    NORTHWEST: QPointF(95, 94),
                }

            return adjustments.get(arrow.loc, QPointF(0, 0))

        else:
            return QPointF(0, 0)

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
        return rotation_adjustments.get(arrow.loc, QPointF(0, 0))
