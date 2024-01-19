from typing import TYPE_CHECKING, Tuple
from constants import NORTH, SOUTH, WEST, EAST, IN, OUT, CLOCK, COUNTER
from PyQt6.QtCore import QPointF

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropOffsetCalculator:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def get_offset(self, prop_length, prop_width) -> Tuple[int, int]:
        offset_map = {}
        if self.prop.ori == IN:
            offset_map = {
                NORTH: (prop_width, 0),
                SOUTH: (0, prop_length),
                WEST: (0, 0),
                EAST: (prop_length, prop_width),
            }
        elif self.prop.ori == OUT:
            offset_map = {
                NORTH: (0, prop_length),
                SOUTH: (prop_width, 0),
                WEST: (prop_length, prop_width),
                EAST: (0, 0),
            }
        elif self.prop.ori == CLOCK:
            offset_map = {
                NORTH: (0, 0),
                SOUTH: (prop_length, prop_width),
                WEST: (0, prop_length),
                EAST: (prop_width, 0),
            }
        elif self.prop.ori == COUNTER:
            offset_map = {
                NORTH: (prop_length, prop_width),
                SOUTH: (0, 0),
                WEST: (prop_width, 0),
                EAST: (0, prop_length),
            }

        offset_tuple = offset_map.get(self.prop.loc, (0, 0))
        return QPointF(offset_tuple[0], offset_tuple[1])
