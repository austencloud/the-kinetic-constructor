from typing import TYPE_CHECKING, Dict, Union

from constants import *
from utilities.TypeChecking.MotionAttributes import (
    Colors,
    Locations,
    Turns,
    MotionTypes,
)


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropAttrManager:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def update_attributes(
        self, prop_dict: Dict[str, Union[Colors, Locations, MotionTypes, Turns]]
    ) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, AXIS, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            value = prop_dict.get(attr)
            if value is not None:
                setattr(self.prop, attr, value)

    def clear_attributes(self) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, AXIS, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            setattr(self.prop, attr, None)
            
