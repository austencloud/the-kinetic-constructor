from typing import TYPE_CHECKING, Dict, Union
from Enums import PropAttribute

from constants import *
from utilities.TypeChecking.MotionAttributes import (
    Colors,
    Locations,
    Orientations,
    Turns,
    MotionTypes,
)
from utilities.TypeChecking.TypeChecking import Axes
from utilities.TypeChecking.prop_types import PropTypes


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropAttrManager:
    def __init__(self, prop: "Prop") -> None:
        self.p = prop
        self.update_attributes(self.p.prop_dict)

    def update_attributes(
        self, prop_dict: Dict[str, Union[Colors, Locations, MotionTypes, Turns]]
    ) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, AXIS, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            value = prop_dict.get(attr)
            if value is not None:
                setattr(self.p, attr, value)

    def clear_attributes(self) -> None:
        prop_attributes = [COLOR, LOC, LAYER, ORI, AXIS, MOTION, PROP_TYPE]
        for attr in prop_attributes:
            setattr(self.p, attr, None)

    def get_axis_from_ori(self) -> None:
        if self.p.check.is_radial():
            axis: Axes = VERTICAL if self.p.loc in [NORTH, SOUTH] else HORIZONTAL
        elif self.p.check.is_nonradial():
            axis: Axes = HORIZONTAL if self.p.loc in [NORTH, SOUTH] else VERTICAL
        else:
            axis: Axes = None
        return axis

    def swap_ori(self) -> None:
        ori_map = {
            IN: OUT,
            OUT: IN,
            CLOCK: COUNTER,
            COUNTER: CLOCK,
        }
        self.ori = ori_map[self.ori]

    def get_attributes(self) -> Dict[str, Union[Colors, Locations, Orientations]]:
        prop_attributes = [attr.value for attr in PropAttribute]
        return {attr: getattr(self, attr) for attr in prop_attributes}

    def update_prop_type(self, prop_type: PropTypes) -> None:
        self.prop_type = prop_type
        self.p.svg_manager.update_svg()
        self.p.updater.update_prop()
