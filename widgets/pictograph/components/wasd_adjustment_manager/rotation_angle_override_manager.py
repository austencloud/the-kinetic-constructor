from typing import TYPE_CHECKING, Optional
from Enums import LetterType
from constants import BLUE, CLOCK, COUNTER, IN, OUT, RED, STATIC, Type2, Type4, Type6
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
        if self.pictograph.selected_arrow.motion.start_ori in [IN, OUT]:
            ori_key = "from_radial"
        elif self.pictograph.selected_arrow.motion.start_ori in [CLOCK, COUNTER]:
            ori_key = "from_nonradial"
            
        data = self.pictograph.main_widget.load_special_placements()

        letter = self.pictograph.letter
        letter_type = LetterType.get_letter_type(letter)

        if letter_type == Type2:
            shift = self.pictograph.get.shift()
            static = self.pictograph.get.static()

            if static.turns > 0:
                direction = "s" if static.prop_rot_dir == shift.prop_rot_dir else "o"
                adjustment_key_str = f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
            letter_data = data[ori_key].get(letter, {})
            turn_data = letter_data.get(adjustment_key_str, {})

            if "static_rot_angle" in turn_data:
                del turn_data["static_rot_angle"]
            else:
                turn_data["static_rot_angle"] = 0

        elif letter in ["Λ", "Λ-"]:
            adjustment_key_str = (
                self.special_positioner.turns_tuple_generator.generate_turns_tuple(
                    letter
                )
            )
            letter_data = data.get(letter, {})
            turn_data = letter_data.get(adjustment_key_str, {})

            if "static_rot_angle" in turn_data:
                del turn_data["static_rot_angle"]
            else:
                turn_data["static_rot_angle"] = 0

            letter_data[adjustment_key_str] = turn_data
            data[letter] = letter_data
            self.special_positioner.data_updater.update_specific_entry_in_json(
                letter, letter_data
            )
            self.pictograph.updater.update_pictograph()

        elif letter_type == Type4:
            dash = self.pictograph.get.dash()
            static = self.pictograph.get.static()

            # Determine the adjustment key based on motion turns
            if static.turns > 0 and dash.turns > 0:
                direction = "s" if static.prop_rot_dir == dash.prop_rot_dir else "o"
                adjustment_key_str = f"({direction}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
            elif static.turns > 0:
                direction = static.prop_rot_dir.lower()  # 'cw' or 'ccw'
                adjustment_key_str = f"({direction}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
            letter_data = data.get(letter, {})
            turn_data = letter_data.get(adjustment_key_str, {})
            if "static_rot_angle" in turn_data:
                del turn_data["static_rot_angle"]
            else:
                turn_data["static_rot_angle"] = 0

        elif letter_type == Type6:
            blue_static = self.pictograph.blue_motion
            red_static = self.pictograph.red_motion

            # Determine the adjustment key based on motion turns
            if blue_static.turns > 0 and red_static.turns > 0:
                direction = (
                    "s" if blue_static.prop_rot_dir == red_static.prop_rot_dir else "o"
                )

                adjustment_key_str = (
                    self.special_positioner.turns_tuple_generator._generate_Γ_key()
                    if letter == "Γ"
                    else f"({direction}, {self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)})"
                )
            elif blue_static.turns > 0 or red_static.turns > 0:
                if blue_static.turns > 0:
                    direction = blue_static.prop_rot_dir.lower()  # 'cw' or 'ccw'
                elif red_static.turns > 0:
                    direction = red_static.prop_rot_dir.lower()  # 'cw' or 'ccw'
                adjustment_key_str = (
                    self.special_positioner.turns_tuple_generator._generate_Γ_key()
                    if letter == "Γ"
                    else f"({direction}, {self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)})"
                )
            letter_data = data.get(letter, {})
            turn_data = letter_data.get(adjustment_key_str, {})
            if self.pictograph.selected_arrow.color == BLUE:
                if "blue_rot_angle" in turn_data:
                    del turn_data["blue_rot_angle"]
                else:
                    turn_data["blue_rot_angle"] = 0
            elif self.pictograph.selected_arrow.color == RED:
                if "red_rot_angle" in turn_data:
                    del turn_data["red_rot_angle"]
                else:
                    turn_data["red_rot_angle"] = 0
        letter_data[adjustment_key_str] = turn_data
        data[letter] = letter_data
        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter, letter_data, self.pictograph.selected_arrow
        )
        self.pictograph.updater.update_pictograph()

    def get_rot_angle_override_from_placements_dict(
        self, arrow: Arrow
    ) -> Optional[int]:
        placements = (
            self.special_positioner.placement_manager.pictograph.main_widget.special_placements
        )
        letter = arrow.scene.letter
        letter_data: dict[str, dict] = placements.get(letter, {})
        turns_tuple = (
            self.special_positioner.turns_tuple_generator.generate_turns_tuple(letter)
        )

        # Check if the letter is of Type 6 and if so, use color to get the rotation angle override
        letter_type = LetterType.get_letter_type(letter)
        if letter_type == Type6:
            return letter_data.get(turns_tuple, {}).get(
                f"{arrow.color}_rot_angle"  # Using color instead of motion type for Type 6
            )
        else:
            return letter_data.get(turns_tuple, {}).get(
                f"{arrow.motion.motion_type}_rot_angle"
            )

    def _normalize_turns(self, arrow: Arrow) -> str:
        """Normalize arrow turns to a string representation."""
        return (
            str(int(arrow.turns))
            if arrow.turns in {0.0, 1.0, 2.0, 3.0}
            else str(arrow.turns)
        )
