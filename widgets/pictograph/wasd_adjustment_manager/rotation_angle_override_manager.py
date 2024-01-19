from typing import TYPE_CHECKING
from constants import BLUE, RED, STATIC
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class RotationAngleOverrideManager:
    def __init__(self, pictograph: "Pictograph"):
        self.pictograph = pictograph

    def handle_rotation_angle_override(self, key):
        if (
            not self.pictograph.selected_arrow
            or self.pictograph.selected_arrow.motion.motion_type != STATIC
        ):
            return

        if key != Qt.Key.Key_X:
            return

        data = (
            self.pictograph.arrow_placement_manager.special_positioner._load_placements()
        )

        static_motion = (
            self.pictograph.motions[RED]
            if self.pictograph.motions[RED].is_static()
            else self.pictograph.motions[BLUE]
        )
        shift_motion = (
            self.pictograph.motions[BLUE]
            if self.pictograph.motions[BLUE].is_shift()
            else self.pictograph.motions[RED]
        )
        if static_motion.turns > 0:
            if static_motion.prop_rot_dir != shift_motion.prop_rot_dir:
                direction = "opp"
            elif static_motion.prop_rot_dir == shift_motion.prop_rot_dir:
                direction = "same"

            direction_prefix = direction[0]
            adjustment_key_str = (
                f"({direction_prefix}, {shift_motion.turns}, {static_motion.turns})"
            )
        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(adjustment_key_str, {})

        if "static_rot_angle" in turn_data:
            del turn_data["static_rot_angle"]
        else:
            turn_data["static_rot_angle"] = 0

        letter_data[adjustment_key_str] = turn_data
        data[self.pictograph.letter] = letter_data
        self.pictograph.arrow_placement_manager.special_positioner.update_specific_entry_in_json(
            self.pictograph.letter, adjustment_key_str, turn_data
        )
