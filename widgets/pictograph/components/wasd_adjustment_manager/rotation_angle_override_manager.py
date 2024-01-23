from typing import TYPE_CHECKING, Dict, Optional
from constants import STATIC
from PyQt6.QtCore import Qt

from objects.arrow.arrow import Arrow


if TYPE_CHECKING:
    from ..wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager


class RotationAngleOverrideManager:
    def __init__(self, wasd_adjustment_manager: "WASD_AdjustmentManager") -> None:
        self.wasd_manager = wasd_adjustment_manager
        self.wasd_manager.pictograph = wasd_adjustment_manager.pictograph
        self.special_positioner = (
            self.wasd_manager.pictograph.arrow_placement_manager.special_positioner
        )

    def handle_rotation_angle_override(self, key) -> None:
        if (
            not self.wasd_manager.pictograph.selected_arrow
            or self.wasd_manager.pictograph.selected_arrow.motion.motion_type != STATIC
        ):
            return

        if key != Qt.Key.Key_X:
            return

        data = self.special_positioner.special_placements

        non_static = (
            self.wasd_manager.pictograph.get.shift()
            if self.wasd_manager.pictograph.get.shift()
            else self.wasd_manager.pictograph.get.dash()
        )
        static = self.wasd_manager.pictograph.get.static()

        if static.turns > 0:
            if static.prop_rot_dir != non_static.prop_rot_dir:
                direction = "opp"
            elif static.prop_rot_dir == non_static.prop_rot_dir:
                direction = "same"

            direction_prefix = direction[0]
            adjustment_key_str = (
                f"({direction_prefix}, {non_static.turns}, {static.turns})"
            )
        letter_data = data.get(self.wasd_manager.pictograph.letter, {})
        turn_data = letter_data.get(adjustment_key_str, {})

        if "static_rot_angle" in turn_data:
            del turn_data["static_rot_angle"]
        else:
            turn_data["static_rot_angle"] = 0

        letter_data[adjustment_key_str] = turn_data
        data[self.wasd_manager.pictograph.letter] = letter_data
        self.special_positioner.data_updater.update_specific_entry_in_json(
            self.wasd_manager.pictograph.letter, adjustment_key_str, turn_data
        )
        self.wasd_manager.pictograph.updater.update_pictograph()

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = self.special_positioner.special_placements
        letter = arrow.scene.letter
        letter_data: Dict[str, Dict] = placements.get(letter, {})
        turns_tuple = (
            self.special_positioner.turns_tuple_generator.generate_turns_tuple(letter)
        )
        return letter_data.get(turns_tuple, {}).get(
            f"{arrow.motion.motion_type}_rot_angle"
        )
