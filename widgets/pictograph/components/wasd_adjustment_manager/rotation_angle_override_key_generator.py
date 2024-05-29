from typing import TYPE_CHECKING
from data.constants import CLOCK, COUNTER, IN, OUT
from objects.arrow.arrow import Arrow

if TYPE_CHECKING:
    from .rotation_angle_override_manager import RotationAngleOverrideManager


class RotationAngleOverrideKeyGenerator:
    def __init__(self, manager: "RotationAngleOverrideManager"):
        self.manager = manager

    def get_layer(self, arrow: Arrow) -> str:
        if arrow.motion.start_ori in [IN, OUT]:
            return "layer1"
        elif arrow.motion.start_ori in [CLOCK, COUNTER]:
            return "layer2"

    def generate_rotation_angle_override_key(self, arrow: Arrow) -> str:
        motion_type = arrow.motion.motion_type
        if arrow.pictograph.check.starts_from_mixed_orientation():
            layer = self.get_layer(arrow)
            return f"{motion_type}_from_{layer}_rot_angle_override"
        return f"{motion_type}_rot_angle_override"


