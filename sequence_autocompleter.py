from typing import TYPE_CHECKING, List, Dict
from position_maps import position_map_cw, position_map_ccw

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SequenceAutocompleter:
    def __init__(self, beat_frame: "SW_BeatFrame"):
        self.json_manager = beat_frame.json_manager
        self.beat_frame = beat_frame

    def perform_auto_completion(self, sequence: List[Dict]):
        start_position_entry = (
            sequence[0] if "sequence_start_position" in sequence[0] else None
        )

        if start_position_entry:
            sequence = sequence[1:]
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]
        last_position = last_entry["end_pos"]
        direction = self.get_hand_rot_dir(sequence)

        new_entries = []
        next_beat_number = last_entry["beat"] + 1

        entries_to_add = self.determine_how_many_entries_to_add()
        if sequence_length == 1:
            for _ in range(entries_to_add):
                new_entry = self.create_new_entry_for_single_beat_sequence(
                    sequence, last_entry, last_position, direction, next_beat_number
                )
                new_entries.append(new_entry)
                last_entry = new_entry
                last_position = new_entry["end_pos"]
                next_beat_number += 1

            if start_position_entry:
                start_position_entry["beat"] = 0
                sequence.insert(0, start_position_entry)

        sequence.extend(new_entries)
        self.json_manager.loader_saver.save_current_sequence(sequence)
        self.beat_frame.populate_beat_frame_from_json(sequence)

    def determine_how_many_entries_to_add(self):
        current_length_of_sequence = (
            self.get_current_length_of_sequence_by_reading_json()
        )
        is_quartered_permutation = self.determine_if_rotation_permutation_is_quartered()
        is_halved_permutation = self.determine_if_rotation_permutation_is_halved()

        if is_quartered_permutation:
            entries = current_length_of_sequence * 3
        elif is_halved_permutation:
            entries = current_length_of_sequence
        else:
            entries = 0

        return entries

    def get_current_length_of_sequence_by_reading_json(self):
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        return len(sequence) - 2

    def determine_if_rotation_permutation_is_quartered(self):
        sequence_start_position = (
            self.json_manager.loader_saver.load_current_sequence_json()[1]["end_pos"]
        )
        end_pos_of_sequence_before_permutation = (
            self.json_manager.loader_saver.load_current_sequence_json()[-1]["end_pos"]
        )

        quartered_permutations = {
            ("alpha1", "alpha2"),
            ("alpha2", "alpha3"),
            ("alpha3", "alpha4"),
            ("alpha4", "alpha1"),
            ("alpha1", "alpha4"),
            ("alpha4", "alpha3"),
            ("alpha3", "alpha2"),
            ("alpha2", "alpha1"),
            ("beta1", "beta2"),
            ("beta2", "beta3"),
            ("beta3", "beta4"),
            ("beta4", "beta1"),
            ("beta1", "beta4"),
            ("beta4", "beta3"),
            ("beta3", "beta2"),
            ("beta2", "beta1"),
            ("gamma1", "gamma2"),
            ("gamma2", "gamma3"),
            ("gamma3", "gamma4"),
            ("gamma4", "gamma1"),
            ("gamma1", "gamma4"),
            ("gamma4", "gamma3"),
            ("gamma3", "gamma2"),
            ("gamma2", "gamma1"),
            ("gamma5", "gamma6"),
            ("gamma6", "gamma7"),
            ("gamma7", "gamma8"),
            ("gamma8", "gamma5"),
            ("gamma5", "gamma8"),
            ("gamma8", "gamma7"),
            ("gamma7", "gamma6"),
            ("gamma6", "gamma5"),
        }

        return (
            sequence_start_position,
            end_pos_of_sequence_before_permutation,
        ) in quartered_permutations

    def determine_if_rotation_permutation_is_halved(self):
        sequence_start_position = (
            self.json_manager.loader_saver.load_current_sequence_json()[1]["end_pos"]
        )
        end_pos_of_sequence_before_permutation = (
            self.json_manager.loader_saver.load_current_sequence_json()[-1]["end_pos"]
        )
        halved_permutations = {
            ("alpha1", "alpha3"),
            ("alpha2", "alpha4"),
            ("alpha3", "alpha1"),
            ("alpha4", "alpha2"),
            ("beta1", "beta3"),
            ("beta2", "beta4"),
            ("beta3", "beta1"),
            ("beta4", "beta2"),
            ("gamma1", "gamma3"),
            ("gamma2", "gamma4"),
            ("gamma3", "gamma1"),
            ("gamma4", "gamma2"),
            ("gamma5", "gamma7"),
            ("gamma6", "gamma8"),
            ("gamma7", "gamma5"),
            ("gamma8", "gamma6"),
        }
        return (
            sequence_start_position,
            end_pos_of_sequence_before_permutation,
        ) in halved_permutations

    def create_new_entry_for_single_beat_sequence(
        self,
        sequence,
        previous_entry: Dict,
        last_position: str,
        direction: str,
        beat_number: int,
    ) -> Dict:
        new_entry = {}

        new_entry["beat"] = beat_number
        new_entry["letter"] = previous_entry["letter"]
        new_entry["start_pos"] = last_position
        new_entry["end_pos"] = self.calculate_new_end_pos(last_position, direction)
        new_entry["timing"] = previous_entry["timing"]
        new_entry["direction"] = previous_entry["direction"]

        blue_attributes = previous_entry["blue_attributes"]
        red_attributes = previous_entry["red_attributes"]

        hand_rot_dir = self.get_hand_rot_dir(sequence)

        new_entry["blue_attributes"] = {
            "motion_type": blue_attributes["motion_type"],
            "start_ori": blue_attributes["end_ori"],
            "prop_rot_dir": blue_attributes["prop_rot_dir"],
            "start_loc": blue_attributes["end_loc"],
            "end_loc": self.calculate_new_loc(
                blue_attributes["end_loc"],
                hand_rot_dir,
                blue_attributes["motion_type"],
            ),
            "turns": blue_attributes["turns"],
        }

        new_entry["red_attributes"] = {
            "motion_type": red_attributes["motion_type"],
            "start_ori": red_attributes["end_ori"],
            "prop_rot_dir": red_attributes["prop_rot_dir"],
            "start_loc": red_attributes["end_loc"],
            "end_loc": self.calculate_new_loc(
                red_attributes["end_loc"],
                hand_rot_dir,
                red_attributes["motion_type"],
            ),
            "turns": red_attributes["turns"],
        }

        new_entry["blue_attributes"]["end_ori"] = (
            self.json_manager.ori_calculator.calculate_end_orientation(
                new_entry, "blue"
            )
        )
        new_entry["red_attributes"]["end_ori"] = (
            self.json_manager.ori_calculator.calculate_end_orientation(new_entry, "red")
        )

        return new_entry

    def get_hand_rot_dir(self, sequence: list[dict]) -> str:
        # look at the very start pos of the sequence. Compare it to the end pos of the last entry
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        # determine if the hand rotation is cw or ccw
        if (start_pos, end_pos) in position_map_cw.items():
            hand_rot_dir = "cw"
        else:
            hand_rot_dir = "ccw"

        return hand_rot_dir

    def calculate_new_end_pos(self, last_position: str, direction: str) -> str:
        pos_map = position_map_cw if direction == "cw" else position_map_ccw
        return pos_map.get(last_position, "alpha1")

    def calculate_new_loc(
        self, start_loc: str, hand_rot_dir: str, motion_type: str
    ) -> str:
        if hand_rot_dir == "cw":
            loc_map = {"s": "w", "w": "n", "n": "e", "e": "s"}
        else:  # ccw
            loc_map = {"s": "e", "e": "n", "n": "w", "w": "s"}

        return loc_map.get(start_loc, "s")
