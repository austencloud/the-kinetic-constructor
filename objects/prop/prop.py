from typing import TYPE_CHECKING, Dict

from objects.graphical_object.graphical_object import GraphicalObject
from objects.prop.prop_attr_manager import PropAttrManager
from objects.prop.prop_checker import PropChecker
from objects.prop.prop_mouse_event_handler import PropMouseEventHandler
from objects.prop.prop_offset_calculator import PropOffsetCalculator
from objects.prop.prop_rot_angle_manager import PropRotAngleManager
from objects.prop.prop_updater import PropUpdater
from utilities.TypeChecking.TypeChecking import (
    Axes,
    Locations,
    Orientations,
)
from utilities.TypeChecking.prop_types import PropTypes


if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow
    from widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion


class Prop(GraphicalObject):
    loc: Locations
    ori: Orientations
    axis: Axes
    prop_type: PropTypes

    def __init__(self, scene, prop_dict: Dict, motion: "Motion") -> None:
        super().__init__(scene)
        self.motion = motion
        self.scene: Pictograph = scene
        self.arrow: Arrow
        self.ghost: Prop = None
        self.is_ghost: bool = False
        self.previous_location: Locations
        self.prop_dict = prop_dict
        self.attr_manager = PropAttrManager(self)
        self.rot_angle_manager = PropRotAngleManager(self)
        self.mouse_event_handler = PropMouseEventHandler(self)
        self.prop_updater = PropUpdater(self)
        self.check = PropChecker(self)
        self.offest_calculator = PropOffsetCalculator(self)
        self.updater = PropUpdater(self)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press()

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)
