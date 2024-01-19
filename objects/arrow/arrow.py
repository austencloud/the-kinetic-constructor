from constants import *
from objects.arrow.arrow_attr_manager import ArrowAttrManager
from objects.arrow.arrow_mirror_manager import ArrowMirrorManager
from objects.arrow.arrow_mouse_event_handler import ArrowMouseEventHandler
from objects.arrow.arrow_updater import ArrowUpdater
from .arrow_location_manager import ArrowLocationCalculator
from .arrow_rot_angle_manager import ArrowRotAngleCalculator
from ..graphical_object.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    MotionTypes,
    Turns,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from .ghost_arrow import GhostArrow
    from widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    svg_cache = {}
    turns: Turns
    motion: "Motion"
    color: Colors
    location: Locations
    loc: Locations

    def __init__(self, pictograph, arrow_dict) -> None:
        super().__init__(pictograph)
        self.arrow_dict = arrow_dict
        self.scene: Pictograph = pictograph
        self.mouse_event_handler = ArrowMouseEventHandler(self)
        self.rot_angle_calculator = ArrowRotAngleCalculator(self)
        self.location_calculator = ArrowLocationCalculator(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        self.updater = ArrowUpdater(self)
        self.ghost: "GhostArrow" = None
        self.loc = None

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.hand_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)
