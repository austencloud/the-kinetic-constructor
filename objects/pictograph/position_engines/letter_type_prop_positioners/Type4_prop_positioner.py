from ..prop_positioners.base_prop_positioner import BasePropPositioner
from Enums import non_strictly_placed_props, strictly_placed_props


class Type4PropPositioner(BasePropPositioner):
    def reposition_Ψ(self) -> None:
        if self.red_prop.prop_type in non_strictly_placed_props:
            direction = self._get_translation_dir_for_non_shift(self.red_prop)
            if direction:
                self._move_prop(self.red_prop, direction)
                self._move_prop(self.blue_prop, self._get_opposite_direction(direction))

        elif self.red_prop.prop_type in strictly_placed_props:
            self._set_prop_to_default_location(self.red_prop)
