from typing import TYPE_CHECKING, Dict
from constants import STATIC
if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class RotationAngleManager:
    def __init__(self, pictograph: "Pictograph"):
        self.pictograph = pictograph

    def handle_rotation_angle_override(self):
        if not self.pictograph.selected_arrow or self.pictograph.selected_arrow.motion.motion_type != STATIC:
            return

        data: Dict = self.pictograph.arrow_placement_manager.special_placement_manager.load_json_data()
        adjustment_key = self.pictograph.arrow_placement_manager.generate_adjustment_key()

        letter_data: Dict = data.get(self.pictograph.letter, {})
        if adjustment_key in letter_data:
            turn_data = letter_data.get(adjustment_key, {})
            turn_data["static_rot_angle"] = 0
            letter_data[adjustment_key] = turn_data
            data[self.pictograph.letter] = letter_data
            self.pictograph.arrow_placement_manager.special_placement_manager.save_json_data(data)
