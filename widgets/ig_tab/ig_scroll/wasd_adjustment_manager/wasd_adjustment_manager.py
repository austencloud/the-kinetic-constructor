from .arrow_movement_manager import ArrowMovementManager

from .rotation_angle_override_manager import RotationAngleOverrideManager


class WASD_AdjustmentManager:
    def __init__(self, pictograph) -> None:
        self.movement_manager = ArrowMovementManager(pictograph)
        self.rotation_manager = RotationAngleOverrideManager(pictograph)
        self.pictograph = pictograph
