from .managers.location_manager.arrow_location_manager import ArrowLocationManager
from .managers.arrow_mirror_handler import ArrowMirrorHandler
from .managers.arrow_mouse_event_handler import ArrowMouseEventHandler
from .managers.arrow_updater import ArrowUpdater
from .managers.arrow_attr_handler import ArrowAttrHandler
from .managers.rot_angle_manager.arrow_rot_angle_manager import ArrowRotAngleManager

from ..graphical_object.graphical_object import GraphicalObject
from Enums.MotionAttributes import Color, Location, Turns
from Enums.Enums import Handpaths
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from widgets.pictograph.pictograph import Pictograph


class Arrow(GraphicalObject):
    """
    An arrow graphical object that can be added to a pictograph as part of a motion.

    Parameters
    ----------
    pictograph : Pictograph
        The pictograph to which the arrow belongs.
    arrow_dict : dict
        A dictionary containing the arrow's attributes.

    """

    svg_cache = {}
    turns: Turns
    motion: "Motion"
    color: Color
    location: Location
    is_svg_mirrored: bool
    loc: Location = None
    initialized: bool = False

    def __init__(self, pictograph, arrow_dict) -> None:
        super().__init__(pictograph)
        self.arrow_dict = arrow_dict
        self.pictograph: Pictograph = pictograph

    def setup_components(self):
        self.location_calculator = ArrowLocationManager(self)
        self.mouse_event_handler = ArrowMouseEventHandler(self)
        self.rot_angle_calculator = ArrowRotAngleManager(self)
        self.mirror_manager = ArrowMirrorHandler(self)
        self.attr_manager = ArrowAttrHandler(self)
        self.updater = ArrowUpdater(self)
        self.initialized = True

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)
