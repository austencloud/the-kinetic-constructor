from .arrow_movement_manager import ArrowMovementManager

from .rotation_angle_override_manager import RotationAngleOverrideManager
from .turn_adjustment_manager import TurnAdjustmentManager


class WASD_AdjustmentManager:
    def __init__(self, pictograph) -> None:
        self.turn_manager = TurnAdjustmentManager(pictograph)
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_manager = RotationAngleOverrideManager(pictograph)
        self.pictograph = pictograph
