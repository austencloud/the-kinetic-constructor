from typing import TYPE_CHECKING

from constants import IN, OUT

if TYPE_CHECKING:
    from .wasd_adjustment_manager import WASD_AdjustmentManager


class PropPlacementOverrideManager:
    def __init__(self, wasd_manager: "WASD_AdjustmentManager") -> None:
        self.pictograph = wasd_manager.pictograph
        self.special_positioner = (
            self.pictograph.arrow_placement_manager.special_positioner
        )

    def handle_prop_placement_override(self, key) -> None:
        if not (
            self.pictograph.check.has_all_nonradial_props()
            or self.pictograph.check.has_all_radial_props()
        ):
            return

        special_placements = self.pictograph.main_widget.special_placements

        letter = self.pictograph.letter
        if self.pictograph.check.has_all_nonradial_props():
            beta_state = "nonradial"
        elif self.pictograph.check.has_all_radial_props():
            beta_state = "radial"

        if self.pictograph.check.has_props_in_beta():
            adjustment_key_str = self._generate_adjustment_key_str(letter)
            orientation_key = self._determine_orientation_key()
            override_key = self._generate_override_key(beta_state)

            letter_data = self._get_letter_data(orientation_key, letter)
            turn_data = self._get_turn_data(letter_data, adjustment_key_str)

            if override_key in turn_data:
                del turn_data[override_key]
            else:
                turn_data[override_key] = True

            letter_data[adjustment_key_str] = turn_data
            special_placements[orientation_key][letter] = letter_data
            self._update_json_entry(letter, letter_data)
            self.pictograph.updater.update_pictograph()

    def _generate_adjustment_key_str(self, letter) -> str:
        return self.special_positioner.turns_tuple_generator.generate_turns_tuple(
            letter
        )

    def _determine_orientation_key(self) -> str:
        if self.pictograph.blue_prop.motion.start_ori in [IN, OUT]:
            return "from_radial"
        else:
            return "from_nonradial"

    def _generate_override_key(self, beta_state) -> str:
        return (
            f"swap_beta_{self.pictograph.blue_prop.loc}_{beta_state}_"
            f"blue_{self.pictograph.blue_motion.motion_type}_{self.pictograph.blue_arrow.loc}_"
            f"red_{self.pictograph.red_motion.motion_type}_{self.pictograph.red_arrow.loc}"
        )

    def _get_letter_data(self, orientation_key, letter) -> dict:
        return self.pictograph.main_widget.special_placements[orientation_key].get(
            letter, {}
        )

    def _get_turn_data(self, letter_data, adjustment_key_str) -> dict:
        return letter_data.get(adjustment_key_str, {})

    def _update_json_entry(self, letter, letter_data) -> None:
        self.special_positioner.data_updater.update_specific_entry_in_json(
            letter, letter_data, self.pictograph.blue_prop
        )
