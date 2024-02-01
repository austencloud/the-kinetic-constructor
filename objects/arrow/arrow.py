from objects.arrow.managers.arrow_mirror_handler import ArrowMirrorHandler
from objects.arrow.managers.arrow_mouse_event_handler import ArrowMouseEventHandler
from objects.arrow.managers.arrow_updater import ArrowUpdater
from objects.arrow.managers.arrow_attr_handler import ArrowAttrHandler
from .managers.arrow_location_manager import ArrowLocationCalculator
from .managers.arrow_rot_angle_calculator import ArrowRotAngleCalculator
from ..graphical_object.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
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
    is_svg_mirrored: bool

    def __init__(self, pictograph, arrow_dict) -> None:
        super().__init__(pictograph)
        self.arrow_dict = arrow_dict
        self.scene: Pictograph = pictograph
        self.mouse_event_handler = ArrowMouseEventHandler(self)
        self.rot_angle_calculator = ArrowRotAngleCalculator(self)
        self.location_calculator = ArrowLocationCalculator(self)
        self.mirror_manager = ArrowMirrorHandler(self)
        self.attr_manager = ArrowAttrHandler(self)
        self.updater = ArrowUpdater(self)
        self.ghost: "GhostArrow" = None
        self.loc = None

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)
