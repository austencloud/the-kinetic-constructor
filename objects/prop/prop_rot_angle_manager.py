from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from data.constants import IN, OUT, CLOCK, COUNTER, NORTH, SOUTH, WEST, EAST

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropRotAngleManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def get_rotation_angle(self) -> int:
        angle_map = {
            IN: {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            OUT: {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            CLOCK: {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            COUNTER: {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }

        key = self.prop.ori
        rotation_angle = angle_map.get(key, {}).get(self.prop.loc, 0)
        return rotation_angle if self.prop.prop_type != PropType.Hand else 0

    def update_prop_rot_angle(self) -> None:
        prop_rotation_angle = self.get_rotation_angle()

        self.prop.setRotation(prop_rotation_angle)
