from Enums import non_strictly_placed_props, strictly_placed_props
from constants import PRO, ANTI
from objects.pictograph.position_engines.prop_positioners.base_prop_positioner import (
    BasePropPositioner,
)


class Type1PropPositioner(BasePropPositioner):
    def reposition_G_H(self) -> None:
        further_direction = self._determine_translation_direction(self.red_motion)
        other_direction = self._get_opposite_direction(further_direction)

        new_red_pos = self._calculate_new_position(
            self.red_prop.pos(), further_direction
        )
        new_blue_pos = self._calculate_new_position(
            self.blue_prop.pos(), other_direction
        )

        self.red_prop.setPos(new_red_pos)
        self.blue_prop.setPos(new_blue_pos)

    def reposition_I(self) -> None:
        pro_prop = (
            self.red_prop if self.red_motion.motion_type == PRO else self.blue_prop
        )
        anti_prop = (
            self.red_prop if self.red_motion.motion_type == ANTI else self.blue_prop
        )
        pro_motion = self.pictograph.motions[pro_prop.color]
        pro_direction = self._determine_translation_direction(pro_motion)
        anti_direction = self._get_opposite_direction(pro_direction)
        new_pro_position = self._calculate_new_position(pro_prop.pos(), pro_direction)
        new_anti_position = self._calculate_new_position(
            anti_prop.pos(), anti_direction
        )
        pro_prop.setPos(new_pro_position)
        anti_prop.setPos(new_anti_position)

    def reposition_J_K_L(self) -> None:
        red_direction = self._determine_translation_direction(self.red_motion)
        blue_direction = self._determine_translation_direction(self.blue_motion)

        if red_direction and blue_direction:
            self._move_prop(self.red_prop, red_direction)
            self._move_prop(self.blue_prop, blue_direction)
