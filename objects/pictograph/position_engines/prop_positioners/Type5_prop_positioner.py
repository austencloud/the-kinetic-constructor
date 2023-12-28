from Enums import non_strictly_placed_props, strictly_placed_props
from objects.pictograph.position_engines.base_prop_positioner import BasePropPositioner

class Type5PropPositioner(BasePropPositioner):
    def reposition_Y_Z(self) -> None:
        if self.scene.main_widget.prop_type in non_strictly_placed_props:
            if self.scene.has_hybrid_orientation():
                for prop in self.props:
                    self._set_default_prop_location(prop)
            else:
                shift = (
                    self.red_motion if self.red_motion.is_shift() else self.blue_motion
                )
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
                        next(
                            prop
                            for prop in self.props
                            if prop.color == static_motion.color
                        ),
                        self._get_opposite_direction(direction),
                    )
        elif self.scene.main_widget.prop_type in strictly_placed_props:
            for prop in self.props:
                self._set_strict_prop_location(prop)
