from typing import TYPE_CHECKING

from .arrow_movement_manager import ArrowMovementManager
from .rotation_angle_override_manager import RotationAngleOverrideManager

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_angle_override_manager = RotationAngleOverrideManager(self)
