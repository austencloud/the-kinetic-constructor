from typing import TYPE_CHECKING
from ..graphical_object.graphical_object import GraphicalObject
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_rot_angle_manager import PropRotAngleManager
from .prop_updater import PropUpdater

if TYPE_CHECKING:
    from Enums.PropTypes import PropType
    from objects.arrow.arrow import Arrow
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    loc: str
    ori: str
    previous_location: str
    prop_type: "PropType"
    arrow: "Arrow"

    def __init__(self, pictograph, prop_dict: dict, motion: "Motion") -> None:
        super().__init__(pictograph)
        self.motion = motion
        self.prop_dict = prop_dict
        self.pictograph: BasePictograph = pictograph
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.updater = PropUpdater(self)
