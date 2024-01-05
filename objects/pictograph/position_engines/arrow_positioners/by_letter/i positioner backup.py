from typing import TYPE_CHECKING, Tuple
from constants import *
from PyQt6.QtCore import QPointF
from objects.arrow import Arrow

if TYPE_CHECKING:
    from objects.pictograph.position_engines.arrow_positioners.Type1_arrow_positioner import (
        Type1ArrowPositioner,
    )
    from objects.pictograph.pictograph import Pictograph


class I_Positioner:
    def __init__(self, pictograph: "Pictograph", positioner: "Type1ArrowPositioner"):
        self.pictograph = pictograph
        self.positioner = positioner

    def _reposition_I(self) -> None:
        for arrow in self.pictograph.arrows.values():
            adjustment = self._calculate_I_adjustment(arrow)
            self.positioner._apply_shift_adjustment(arrow, adjustment)

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
                elif anti_arrow.turns == 2:
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
                elif anti_arrow.turns == 2.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(5, 55),
                                SOUTHEAST: QPointF(-55, 5),
                                SOUTHWEST: QPointF(-5, -55),
                                NORTHWEST: QPointF(55, -5),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-55, -5),
                                SOUTHEAST: QPointF(5, -55),
                                SOUTHWEST: QPointF(55, 5),
                                NORTHWEST: QPointF(-5, 55),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-60, 110),
                                SOUTHEAST: QPointF(-110, -60),
                                SOUTHWEST: QPointF(60, -110),
                                NORTHWEST: QPointF(110, 60),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-110, 60),
                                SOUTHEAST: QPointF(-60, -110),
                                SOUTHWEST: QPointF(110, -60),
                                NORTHWEST: QPointF(60, 110),
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
            elif pro_arrow.turns == 1:
                if anti_arrow.turns == 0:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-35, -40),
                                SOUTHEAST: QPointF(40, -35),
                                SOUTHWEST: QPointF(35, 40),
                                NORTHWEST: QPointF(-40, 35),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(40, 35),
                                SOUTHEAST: QPointF(-35, 40),
                                SOUTHWEST: QPointF(-40, -35),
                                NORTHWEST: QPointF(35, -40),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(65, -70),
                                SOUTHEAST: QPointF(70, 65),
                                SOUTHWEST: QPointF(-65, 70),
                                NORTHWEST: QPointF(-70, -65),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -65),
                                SOUTHEAST: QPointF(65, 70),
                                SOUTHWEST: QPointF(-70, 65),
                                NORTHWEST: QPointF(-65, -70),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))

                elif anti_arrow.turns == 0.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-45, -60),
                                SOUTHEAST: QPointF(60, -45),
                                SOUTHWEST: QPointF(45, 60),
                                NORTHWEST: QPointF(-60, 45),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(60, 45),
                                SOUTHEAST: QPointF(-45, 60),
                                SOUTHWEST: QPointF(-60, -45),
                                NORTHWEST: QPointF(45, -60),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-85, 115),
                                SOUTHEAST: QPointF(-115, -85),
                                SOUTHWEST: QPointF(85, -115),
                                NORTHWEST: QPointF(115, 85),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-115, 85),
                                SOUTHEAST: QPointF(-85, -115),
                                SOUTHWEST: QPointF(115, -85),
                                NORTHWEST: QPointF(85, 115),
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
                                NORTHEAST: QPointF(-45, -65),
                                SOUTHEAST: QPointF(65, -45),
                                SOUTHWEST: QPointF(45, 65),
                                NORTHWEST: QPointF(-65, 45),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(65, 45),
                                SOUTHEAST: QPointF(-45, 65),
                                SOUTHWEST: QPointF(-65, -45),
                                NORTHWEST: QPointF(45, -65),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-70, 20),
                                SOUTHEAST: QPointF(-20, -70),
                                SOUTHWEST: QPointF(70, -20),
                                NORTHWEST: QPointF(20, 70),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-20, 70),
                                SOUTHEAST: QPointF(-70, -20),
                                SOUTHWEST: QPointF(20, -70),
                                NORTHWEST: QPointF(70, 20),
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
                                NORTHEAST: QPointF(65, -80),
                                SOUTHEAST: QPointF(80, 65),
                                SOUTHWEST: QPointF(-65, 80),
                                NORTHWEST: QPointF(-80, -65),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(80, -65),
                                SOUTHEAST: QPointF(65, 80),
                                SOUTHWEST: QPointF(-80, 65),
                                NORTHWEST: QPointF(-65, -80),
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
                                NORTHEAST: QPointF(-40, 5),
                                SOUTHEAST: QPointF(-5, -40),
                                SOUTHWEST: QPointF(40, -5),
                                NORTHWEST: QPointF(5, 40),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-5, 40),
                                SOUTHEAST: QPointF(-40, -5),
                                SOUTHWEST: QPointF(5, -40),
                                NORTHWEST: QPointF(40, 5),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-85, 115),
                                SOUTHEAST: QPointF(-115, -85),
                                SOUTHWEST: QPointF(85, -115),
                                NORTHWEST: QPointF(115, 85),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-115, 85),
                                SOUTHEAST: QPointF(-85, -115),
                                SOUTHWEST: QPointF(115, -85),
                                NORTHWEST: QPointF(85, 115),
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
                                NORTHEAST: QPointF(65, -80),
                                SOUTHEAST: QPointF(80, 65),
                                SOUTHWEST: QPointF(-65, 80),
                                NORTHWEST: QPointF(-80, -65),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(80, -65),
                                SOUTHEAST: QPointF(65, 80),
                                SOUTHWEST: QPointF(-80, 65),
                                NORTHWEST: QPointF(-65, -80),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )
                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
            elif pro_arrow.turns == 1.5:
                if anti_arrow.turns == 0:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(15, 5),
                                SOUTHEAST: QPointF(-5, 15),
                                SOUTHWEST: QPointF(-15, -5),
                                NORTHWEST: QPointF(5, -15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-5, -15),
                                SOUTHEAST: QPointF(15, -5),
                                SOUTHWEST: QPointF(5, 15),
                                NORTHWEST: QPointF(-15, 5),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(80, -70),
                                SOUTHEAST: QPointF(70, 80),
                                SOUTHWEST: QPointF(-80, 70),
                                NORTHWEST: QPointF(-70, -80),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -80),
                                SOUTHEAST: QPointF(80, 70),
                                SOUTHWEST: QPointF(-70, 80),
                                NORTHWEST: QPointF(-80, -70),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )

                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
                elif anti_arrow.turns == 0.5:
                    adjustments = {
                        PRO: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-10, 5),
                                SOUTHEAST: QPointF(-5, -10),
                                SOUTHWEST: QPointF(10, -5),
                                NORTHWEST: QPointF(5, 10),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-5, 10),
                                SOUTHEAST: QPointF(-10, -5),
                                SOUTHWEST: QPointF(5, -10),
                                NORTHWEST: QPointF(10, -5),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(-75, 130),
                                SOUTHEAST: QPointF(-130, -75),
                                SOUTHWEST: QPointF(75, -130),
                                NORTHWEST: QPointF(130, 75),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-130, 75),
                                SOUTHEAST: QPointF(-75, -130),
                                SOUTHWEST: QPointF(130, -75),
                                NORTHWEST: QPointF(75, 130),
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
                                NORTHEAST: QPointF(15, 5),
                                SOUTHEAST: QPointF(-5, 15),
                                SOUTHWEST: QPointF(-15, -5),
                                NORTHWEST: QPointF(5, -15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-5, -15),
                                SOUTHEAST: QPointF(15, -5),
                                SOUTHWEST: QPointF(5, 15),
                                NORTHWEST: QPointF(-15, 5),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(135, -70),
                                SOUTHEAST: QPointF(70, 135),
                                SOUTHWEST: QPointF(-135, 70),
                                NORTHWEST: QPointF(-70, -135),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -135),
                                SOUTHEAST: QPointF(135, 70),
                                SOUTHWEST: QPointF(-70, 135),
                                NORTHWEST: QPointF(-135, -70),
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
                                NORTHEAST: QPointF(15, 5),
                                SOUTHEAST: QPointF(-5, 15),
                                SOUTHWEST: QPointF(-15, -5),
                                NORTHWEST: QPointF(5, -15),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(-5, -15),
                                SOUTHEAST: QPointF(15, -5),
                                SOUTHWEST: QPointF(5, 15),
                                NORTHWEST: QPointF(-15, 5),
                            },
                        },
                        ANTI: {
                            CLOCKWISE: {
                                NORTHEAST: QPointF(135, -70),
                                SOUTHEAST: QPointF(70, 135),
                                SOUTHWEST: QPointF(-135, 70),
                                NORTHWEST: QPointF(-70, -135),
                            },
                            COUNTER_CLOCKWISE: {
                                NORTHEAST: QPointF(70, -135),
                                SOUTHEAST: QPointF(135, 70),
                                SOUTHWEST: QPointF(-70, 135),
                                NORTHWEST: QPointF(-135, -70),
                            },
                        },
                    }
                    motion_type_adjustments = adjustments.get(arrow.motion_type, {})
                    direction_adjustments = motion_type_adjustments.get(
                        arrow.motion.prop_rot_dir, {}
                    )

                    return direction_adjustments.get(arrow.loc, QPointF(0, 0))
