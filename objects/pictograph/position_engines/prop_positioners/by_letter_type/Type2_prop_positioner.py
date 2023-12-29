from typing import TYPE_CHECKING
from objects.pictograph.position_engines.prop_positioners.base_prop_positioner import (
    BasePropPositioner,
)

if TYPE_CHECKING:
    pass


class Type2PropPositioner(BasePropPositioner):
    def reposition_Y_Z(self) -> None:
        shift = self.red_motion if self.red_motion.is_shift() else self.blue_motion
        static_motion = (
            self.red_motion if self.red_motion.is_static() else self.blue_motion
        )

        direction = self._determine_translation_direction(shift)
        if direction:
            self._move_prop(
                next(prop for prop in self.props if prop.color == shift.color),
                direction,
            )
            self._move_prop(
                next(prop for prop in self.props if prop.color == static_motion.color),
                self._get_opposite_direction(direction),
            )
