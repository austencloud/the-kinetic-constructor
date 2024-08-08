from typing import TYPE_CHECKING
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from data.constants import EAST, NORTH, SOUTH, WEST

from typing import TYPE_CHECKING
from sequence_auto_completer.permutation_executor_base import PermutationExecutor

if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completion_manager import (
        SequenceAutoCompletionManager,
    )

if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completion_manager import (
        SequenceAutoCompletionManager,
    )


class RotationalPermutationExecuter(PermutationExecutor):
    def __init__(self, autocompleter: "SequenceAutoCompletionManager"):
        self.autocompleter = autocompleter

    def create_permutations(self, sequence: list[dict]):
        start_position_entry = (
            sequence.pop(0) if "sequence_start_position" in sequence[0] else None
        )
        sequence_length = len(sequence) - 2
        last_entry = sequence[-1]

        new_entries = []
        next_beat_number = last_entry["beat"] + 1
        halved_or_quartered = self.get_halved_or_quartered()

        entries_to_add = self.determine_how_many_entries_to_add(sequence_length)
        for _ in range(entries_to_add):
            new_entry = self.create_new_rotational_permutation_entry(
                sequence,
                last_entry,
                next_beat_number,
                sequence_length + entries_to_add,
                halved_or_quartered,
                "rotational",
            )
            new_entries.append(new_entry)
            sequence.append(new_entry)
            last_entry = new_entry
            next_beat_number += 1

        if start_position_entry:
            start_position_entry["beat"] = 0
            sequence.insert(0, start_position_entry)

        self.autocompleter.json_manager.loader_saver.save_current_sequence(sequence)
        self.autocompleter.beat_frame.populate_beat_frame_from_json(sequence)

    def determine_how_many_entries_to_add(self, sequence_length: int) -> int:
        if self.is_quartered_permutation():
            return sequence_length * 3
        elif self.is_halved_permutation():
            return sequence_length
        return 0

    def is_quartered_permutation(self) -> bool:
        sequence = (
            self.autocompleter.json_manager.loader_saver.load_current_sequence_json()
        )
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        return (start_pos, end_pos) in quartered_permutations

    def is_halved_permutation(self) -> bool:
        sequence = (
            self.autocompleter.json_manager.loader_saver.load_current_sequence_json()
        )
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        return (start_pos, end_pos) in halved_permutations

    def get_halved_or_quartered(self) -> str:
        if self.is_halved_permutation():
            return "halved"
        elif self.is_quartered_permutation():
            return "quartered"
        return ""

    def calculate_rotational_permuatation_new_loc(
        self, start_loc: str, hand_rot_dir: str
    ) -> str:
        loc_map_cw = {"s": "w", "w": "n", "n": "e", "e": "s"}
        loc_map_ccw = {"s": "e", "e": "n", "n": "w", "w": "s"}
        loc_map = loc_map_cw if hand_rot_dir == "cw" else loc_map_ccw

        if hand_rot_dir == "dash":
            loc_map = {"s": "n", "n": "s", "w": "e", "e": "w"}
        elif hand_rot_dir == "static":
            loc_map = {"s": "s", "n": "n", "w": "w", "e": "e"}

        return loc_map[start_loc]

    def create_new_rotational_permutation_entry(
        self,
        sequence,
        previous_entry,
        beat_number: int,
        final_intended_sequence_length: int,
        halved_or_quartered: str,
        permutation_type: str,
        color_swap: bool = False,
    ) -> dict:
        if permutation_type == "rotational":
            previous_matching_beat = self.get_previous_matching_beat(
                sequence,
                beat_number,
                final_intended_sequence_length,
                halved_or_quartered,
            )
        else:
            previous_matching_beat = self.get_previous_matching_beat_mirrored(
                sequence, beat_number, final_intended_sequence_length, color_swap
            )

        new_entry = {
            "beat": beat_number,
            "letter": previous_matching_beat["letter"],
            "start_pos": previous_entry["end_pos"],
            "end_pos": self.calculate_new_end_pos(
                previous_matching_beat, previous_entry
            ),
            "timing": previous_matching_beat["timing"],
            "direction": previous_matching_beat["direction"],
            "blue_attributes": self.create_new_attributes(
                previous_entry["blue_attributes"],
                previous_matching_beat["blue_attributes"],
            ),
            "red_attributes": self.create_new_attributes(
                previous_entry["red_attributes"],
                previous_matching_beat["red_attributes"],
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

    def calculate_new_end_pos(
        self, previous_matching_beat: dict, previous_entry: dict
    ) -> str:
        new_blue_end_loc = self.autocompleter.rotational_permutation_executor.calculate_rotational_permuatation_new_loc(
            previous_entry["blue_attributes"]["end_loc"],
            self.get_hand_rot_dir_from_locs(
                previous_matching_beat["blue_attributes"]["start_loc"],
                previous_matching_beat["blue_attributes"]["end_loc"],
            ),
        )
        new_red_end_loc = self.autocompleter.rotational_permutation_executor.calculate_rotational_permuatation_new_loc(
            previous_entry["red_attributes"]["end_loc"],
            self.get_hand_rot_dir_from_locs(
                previous_matching_beat["red_attributes"]["start_loc"],
                previous_matching_beat["red_attributes"]["end_loc"],
            ),
        )
        return self.get_numbered_position_from_locs(new_blue_end_loc, new_red_end_loc)

    def get_hand_rot_dir_from_locs(self, start_loc: str, end_loc: str) -> str:
        hand_rot_dir_map = {
            (SOUTH, WEST): "cw",
            (WEST, NORTH): "cw",
            (NORTH, EAST): "cw",
            (EAST, SOUTH): "cw",
            (WEST, SOUTH): "ccw",
            (NORTH, WEST): "ccw",
            (EAST, NORTH): "ccw",
            (SOUTH, EAST): "ccw",
            (SOUTH, NORTH): "dash",
            (WEST, EAST): "dash",
            (NORTH, SOUTH): "dash",
            (EAST, WEST): "dash",
            (NORTH, NORTH): "static",
            (EAST, EAST): "static",
            (SOUTH, SOUTH): "static",
            (WEST, WEST): "static",
        }
        return hand_rot_dir_map.get((start_loc, end_loc))

    def get_numbered_position_from_locs(self, blue_loc: str, red_loc: str) -> str:
        positions_map = {
            (SOUTH, NORTH): "alpha1",
            (WEST, EAST): "alpha2",
            (NORTH, SOUTH): "alpha3",
            (EAST, WEST): "alpha4",
            (NORTH, NORTH): "beta1",
            (EAST, EAST): "beta2",
            (SOUTH, SOUTH): "beta3",
            (WEST, WEST): "beta4",
            (WEST, NORTH): "gamma1",
            (NORTH, EAST): "gamma2",
            (EAST, SOUTH): "gamma3",
            (SOUTH, WEST): "gamma4",
            (EAST, NORTH): "gamma5",
            (SOUTH, EAST): "gamma6",
            (WEST, SOUTH): "gamma7",
            (NORTH, WEST): "gamma8",
        }
        return positions_map.get((blue_loc, red_loc))

    def get_previous_matching_beat(
        self,
        sequence: list[dict],
        beat_number: int,
        final_length: int,
        halved_or_quartered: str,
    ) -> dict:
        index_map = self.get_index_map(halved_or_quartered, final_length)
        return sequence[index_map[beat_number]]

    def get_index_map(self, halved_or_quartered: str, length: int) -> dict[int, int]:
        if halved_or_quartered == "quartered":
            return {
                i: i - (length // 4) + 1 for i in range((length // 4) + 1, length + 1)
            }
        elif halved_or_quartered == "halved":
            return {
                i: i - (length // 2) + 1 for i in range((length // 2) + 1, length + 1)
            }
        return {}

    def get_previous_matching_beat_mirrored(
        self,
        sequence: list[dict],
        beat_number: int,
        final_length: int,
        color_swap: bool,
    ) -> dict:
        mid_point = final_length // 2
        mirrored_beat_number = (final_length - beat_number) % mid_point
        mirrored_beat = sequence[mirrored_beat_number]
        if color_swap:
            mirrored_beat = self.swap_colors(mirrored_beat)
        return mirrored_beat

    def swap_colors(self, beat: dict) -> dict:
        beat["blue_attributes"], beat["red_attributes"] = (
            beat["red_attributes"],
            beat["blue_attributes"],
        )
        return beat

    def create_new_attributes(
        self,
        previous_attributes: dict,
        previous_matching_beat_attributes: dict,
    ) -> dict:
        return {
            "motion_type": previous_matching_beat_attributes["motion_type"],
            "start_ori": previous_attributes["end_ori"],
            "prop_rot_dir": previous_matching_beat_attributes["prop_rot_dir"],
            "start_loc": previous_attributes["end_loc"],
            "end_loc": self.autocompleter.rotational_permutation_executor.calculate_rotational_permuatation_new_loc(
                previous_attributes["end_loc"],
                self.get_hand_rot_dir_from_locs(
                    previous_matching_beat_attributes["start_loc"],
                    previous_matching_beat_attributes["end_loc"],
                ),
            ),
            "turns": previous_matching_beat_attributes["turns"],
        }
