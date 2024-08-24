from typing import TYPE_CHECKING
from ..graphical_object.graphical_object import GraphicalObject
from .prop_attr_manager import PropAttrManager
from .prop_checker import PropChecker
from .prop_mouse_event_handler import PropMouseEventHandler
from .prop_offset_calculator import PropOffsetCalculator
from .prop_rot_angle_manager import PropRotAngleManager
from .prop_updater import PropUpdater
from Enums.MotionAttributes import Location, Orientations
from Enums.Enums import Axes
from Enums.PropTypes import PropType


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    """
    A prop object that can be added to a pictograph.

    Parameters
    ----------
    pictograph : Pictograph
        The pictograph to which the prop belongs.
    prop_dict : dict
        A dictionary containing the prop's attributes.
    motion : Motion
        The motion to which the prop belongs.
    """

    loc: Location
    ori: Orientations = None
    axis: Axes
    prop_type: PropType

    def __init__(self, pictograph, prop_dict: dict, motion: "Motion") -> None:
        super().__init__(pictograph)
        self.motion = motion
        self.scene: Pictograph = pictograph
        self.arrow: Arrow
        self.previous_location: Location
        self.prop_dict = prop_dict
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.check = PropChecker(self)
        self.offest_calculator = PropOffsetCalculator(self)
        self.updater = PropUpdater(self)
