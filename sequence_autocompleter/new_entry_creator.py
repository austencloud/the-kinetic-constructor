from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from sequence_autocompleter.sequence_autocompleter import SequenceAutocompleter


class NewEntryCreator:
    def __init__(self, autocompleter: "SequenceAutocompleter"):
        self.autocompleter = autocompleter

    def create_new_entry(
        self,
        sequence,
        previous_entry: Dict,
        last_position: str,
        direction: str,
        beat_number: int,
    ) -> Dict:
        new_entry = {
            "beat": beat_number,
            "letter": previous_entry["letter"],
            "start_pos": last_position,
            "end_pos": self.autocompleter.calculate_new_end_pos(
                last_position, direction
            ),
            "timing": previous_entry["timing"],
            "direction": previous_entry["direction"],
            "blue_attributes": self.create_new_attributes(
                previous_entry["blue_attributes"], direction
            ),
            "red_attributes": self.create_new_attributes(
                previous_entry["red_attributes"], direction
            ),
        }

        new_entry["blue_attributes"]["end_ori"] = (
            self.autocompleter.json_manager.ori_calculator.calculate_end_orientation(
                new_entry, "blue"
            )
        )
        new_entry["red_attributes"]["end_ori"] = (
            self.autocompleter.json_manager.ori_calculator.calculate_end_orientation(
                new_entry, "red"
            )
        )

        return new_entry

    def create_new_attributes(self, attributes: Dict, direction: str) -> Dict:
        new_attributes = {
            "motion_type": attributes["motion_type"],
            "start_ori": attributes["end_ori"],
            "prop_rot_dir": attributes["prop_rot_dir"],
            "start_loc": attributes["end_loc"],
            "end_loc": self.autocompleter.calculate_new_loc(
                attributes["end_loc"], direction, attributes["motion_type"]
            ),
            "turns": attributes["turns"],
        }
        return new_attributes
