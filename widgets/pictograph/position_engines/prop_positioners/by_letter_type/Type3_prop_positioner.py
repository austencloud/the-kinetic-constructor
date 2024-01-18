


from ..base_prop_positioner import BasePropPositioner


class Type3PropPositioner(BasePropPositioner):
    def reposition_Y_dash_Z_dash(self) -> None:
        shift = self.red_motion if self.red_motion.is_shift() else self.blue_motion
        dash = self.red_motion if self.red_motion.is_dash() else self.blue_motion

        direction = self._determine_translation_direction(shift)
        if direction:
            self._move_prop(
                next(prop for prop in self.props if prop.color == shift.color),
                direction,
            )
            self._move_prop(
                next(prop for prop in self.props if prop.color == dash.color),
                self._get_opposite_direction(direction),
            )
