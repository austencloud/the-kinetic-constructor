from typing import TYPE_CHECKING, Dict, Optional
from constants import STATIC
from PyQt6.QtCore import Qt

from objects.arrow.arrow import Arrow


if TYPE_CHECKING:
    from ..wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager


class RotationAngleOverrideManager:
    def __init__(self, wasd_adjustment_manager: "WASD_AdjustmentManager") -> None:
        self.wasd_manager = wasd_adjustment_manager
        self.pictograph = wasd_adjustment_manager.pictograph
        self.special_positioner = (
            self.pictograph.arrow_placement_manager.special_positioner
        )

    def handle_rotation_angle_override(self, key) -> None:
        if (
            not self.pictograph.selected_arrow
            or self.pictograph.selected_arrow.motion.motion_type != STATIC
        ):
            return

        if key != Qt.Key.Key_X:
            return

        data = self.pictograph.main_widget.load_special_placements()
        non_static = (
            self.pictograph.get.shift()
            if self.pictograph.get.shift()
            else self.pictograph.get.dash()
        )
        static = self.pictograph.get.static()

        # Determine the adjustment key based on motion turns
        if static.turns > 0 and non_static.turns > 0:
            direction = "s" if static.prop_rot_dir == non_static.prop_rot_dir else "o"
            adjustment_key_str = (
                f"({direction}, {self._normalize_turns(non_static)}, {self._normalize_turns(static)})"
            )
        elif static.turns > 0:
            direction = static.prop_rot_dir.lower()  # 'cw' or 'ccw'
            adjustment_key_str = (
                f"({direction}, {self._normalize_turns(non_static)}, {self._normalize_turns(static)})"
            )

        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(adjustment_key_str, {})

        # Toggle the rotation angle override
        if "static_rot_angle" in turn_data:
            del turn_data["static_rot_angle"]
        else:
            turn_data["static_rot_angle"] = 0

        letter_data[adjustment_key_str] = turn_data
        data[self.pictograph.letter] = letter_data
        self.special_positioner.data_updater.update_specific_entry_in_json(
            self.pictograph.letter, letter_data
        )
        self.pictograph.updater.update_pictograph()

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = (
            self.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        letter = arrow.scene.letter
        letter_data: Dict[str, Dict] = placements.get(letter, {})
        turns_tuple = (
            self.special_positioner.turns_tuple_generator.generate_turns_tuple(letter)
        )
        return letter_data.get(turns_tuple, {}).get(
            f"{arrow.motion.motion_type}_rot_angle"
        )

    def _normalize_turns(self, arrow: Arrow) -> str:
        """Normalize arrow turns to a string representation."""
        return str(int(arrow.turns)) if arrow.turns in {0.0, 1.0, 2.0, 3.0} else str(arrow.turns)