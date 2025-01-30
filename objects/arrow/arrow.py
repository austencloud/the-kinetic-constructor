from .location_manager.arrow_loc_manager import ArrowLocationManager
from .arrow_mirror_handler import ArrowMirrorManager
from .arrow_updater import ArrowUpdater
from .arrow_attr_handler import ArrowAttrManager
from .rot_angle_manager.arrow_rot_angle_manager import ArrowRotAngleManager

from ..graphical_object.graphical_object import GraphicalObject
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..motion.motion import Motion
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class Arrow(GraphicalObject):
    motion: "Motion"
    color: str
    is_svg_mirrored: bool
    loc: str = None
    initialized: bool = False

    def __init__(self, pictograph, arrow_data) -> None:
        super().__init__(pictograph)
        self.arrow_data = arrow_data
        self.pictograph: BasePictograph = pictograph

    def setup_components(self):
        self.location_manager = ArrowLocationManager(self)
        self.rot_angle_manager = ArrowRotAngleManager(self)
        self.mirror_manager = ArrowMirrorManager(self)
        self.attr_manager = ArrowAttrManager(self)
        self.updater = ArrowUpdater(self)
        self.initialized = True
