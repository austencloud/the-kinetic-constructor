from typing import TYPE_CHECKING
from constants import CLOCK, COUNTER, IN, OUT

if TYPE_CHECKING:
    from .rotation_angle_override_manager import RotationAngleOverrideManager


class RotationAngleOverrideKeyGenerator:
    def __init__(self, manager: "RotationAngleOverrideManager"):
        self.manager = manager

    def get_layer(self) -> str:
        if self.arrow.motion.start_ori in [IN, OUT]:
            return "layer1"
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            return "layer2"

    def generate_rotation_angle_override_key(self) -> str:
        self.arrow = self.manager.pictograph.selected_arrow
        motion_type = self.arrow.motion.motion_type
        if self.arrow.pictograph.check.starts_from_mixed_orientation():
            layer = self.get_layer()
            return f"{motion_type}_from_{layer}_rot_angle_override"
        return f"{motion_type}_rot_angle_override"

    def generate_hybrid_key(self, base_key: str) -> str:
        if self.arrow.pictograph.check.starts_from_mixed_orientation():
            layer = self.get_layer()
            return f"{base_key}_from_{layer}_override"
        return base_key
