from typing import Union, TYPE_CHECKING

from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
from utilities.TypeChecking.MotionAttributes import (
    Colors,
    Locations,
    MotionTypes,
    Turns,
)


class ArrowAttrHandler:
    def __init__(self, arrow: "Arrow") -> None:
        self.a = arrow
        self.a.color = self.a.arrow_dict[COLOR]
        self.a.turns = self.a.arrow_dict[TURNS]

    def update_attributes(
        self, arrow_dict: dict[str, Union[Colors, Locations, MotionTypes, Turns]]
    ) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            value = arrow_dict.get(attr)
            if value is not None:
                setattr(self.a, attr, value)

    def clear_attributes(self) -> None:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE, TURNS]
        for attr in arrow_attributes:
            setattr(self.a, attr, None)

    def get_arrow_attributes(self) -> dict[str, Union[Colors, Locations, MotionTypes]]:
        arrow_attributes = [COLOR, LOC, MOTION_TYPE]
        return {attr: getattr(self.a, attr) for attr in arrow_attributes}
