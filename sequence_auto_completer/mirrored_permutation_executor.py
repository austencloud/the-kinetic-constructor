from typing import TYPE_CHECKING
from data.constants import EAST, NORTH, SOUTH, WEST
from sequence_auto_completer.permutation_executor_base import PermutationExecutor

if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completion_manager import (
        SequenceAutoCompletionManager,
    )

# Define mirroring maps
vertical_mirror_map = {"s": "s", "e": "w", "w": "e", "n": "n"}

horizontal_mirror_map = {"s": "n", "n": "s", "e": "e", "w": "w"}


class MirroredPermutationExecutor(PermutationExecutor):
    def __init__(
        self,
        autocompleter: "SequenceAutoCompletionManager",
        color_swap_second_half: bool,
    ):
        self.autocompleter = autocompleter
        self.color_swap_second_half = color_swap_second_half

    def create_permutations(self, sequence: list[dict], vertical_or_horizontal: str):
        if not self.can_perform_mirrored_permutation(sequence):
            return
        self.vertical_or_horizontal = vertical_or_horizontal
        sequence_length = len(sequence)
        last_entry = sequence[-1]
        new_entries = []
        next_beat_number = last_entry["beat"] + 1

        for i in range(sequence_length):
            if i in [0, 1]:
                continue
            new_entry = self.create_new_mirrored_permutation_entry(
                last_entry,
                sequence[i],
                next_beat_number + i,
                self.color_swap_second_half,
                vertical_or_horizontal,
            )
            new_entries.append(new_entry)
            sequence.append(new_entry)
            last_entry = new_entry

        self.autocompleter.json_manager.loader_saver.save_current_sequence(sequence)
        self.autocompleter.beat_frame.populate_beat_frame_from_json(sequence)

    def can_perform_mirrored_permutation(self, sequence: list[dict]) -> bool:
        return sequence[1]["end_pos"] == sequence[-1]["end_pos"]

    def create_new_mirrored_permutation_entry(
        self,
        previous_entry,
        previous_matching_beat: dict,
        beat: int,
        color_swap_second_half: bool,
        vertical_or_horizontal: str,
    ) -> dict:
        new_entry = {
            "beat": beat,
            "letter": previous_matching_beat["letter"],
            "start_pos": previous_entry["end_pos"],
            "end_pos": self.get_mirrored_position(
                previous_matching_beat, vertical_or_horizontal
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

        if color_swap_second_half:
            new_entry["blue_attributes"], new_entry["red_attributes"] = (
                new_entry["red_attributes"],
                new_entry["blue_attributes"],
            )

        return new_entry

    def get_mirrored_position(
        self, previous_matching_beat, vertical_or_horizontal
    ) -> str:
        mirrored_positions = {
            "vertical": {
                "alpha1": "alpha1",
                "alpha2": "alpha4",
                "alpha3": "alpha3",
                "alpha4": "alpha2",
                "beta1": "beta1",
                "beta2": "beta4",
                "beta3": "beta3",
                "beta4": "beta2",
                "gamma1": "gamma5",
                "gamma2": "gamma8",
                "gamma3": "gamma7",
                "gamma4": "gamma6",
                "gamma5": "gamma1",
                "gamma6": "gamma4",
                "gamma7": "gamma3",
                "gamma8": "gamma2",
            },
            "horizontal": {
                "alpha1": "alpha3",
                "alpha2": "alpha2",
                "alpha3": "alpha1",
                "alpha4": "alpha4",
                "beta1": "beta3",
                "beta2": "beta2",
                "beta3": "beta1",
                "beta4": "beta4",
                "gamma1": "gamma7",
                "gamma2": "gamma6",
                "gamma3": "gamma5",
                "gamma4": "gamma8",
                "gamma5": "gamma3",
                "gamma6": "gamma2",
                "gamma7": "gamma1",
                "gamma8": "gamma4",
            },
        }
        return mirrored_positions[vertical_or_horizontal][
            previous_matching_beat["end_pos"]
        ]

    def get_mirrored_prop_rot_dir(self, prop_rot_dir: str) -> str:
        if prop_rot_dir == "cw":
            return "ccw"
        elif prop_rot_dir == "ccw":
            return "cw"
        elif prop_rot_dir == "no_rot":
            return "no_rot"

    def create_new_attributes(
        self,
        previous_entry_attributes: dict,
        previous_matching_beat_attributes: dict,
    ) -> dict:
        new_entry_attributes = {
            "motion_type": previous_matching_beat_attributes["motion_type"],
            "start_ori": previous_entry_attributes["end_ori"],
            "prop_rot_dir": self.get_mirrored_prop_rot_dir(
                previous_matching_beat_attributes["prop_rot_dir"]
            ),
            "start_loc": previous_entry_attributes["end_loc"],
            "end_loc": self.calculate_mirrored_permuatation_new_loc(
                previous_matching_beat_attributes["end_loc"]
            ),
            "turns": previous_matching_beat_attributes["turns"],
        }

        return new_entry_attributes

    def calculate_mirrored_permuatation_new_loc(
        self, previous_matching_beat_end_loc: str
    ) -> str:
        if self.vertical_or_horizontal == "vertical":
            return self.get_vertical_mirrored_location(previous_matching_beat_end_loc)
        elif self.vertical_or_horizontal == "horizontal":
            return self.get_horizontal_mirrored_location(previous_matching_beat_end_loc)

    def get_mirrored_rotation(self, rotation: str) -> str:
        if rotation == "cw":
            return "ccw"
        elif rotation == "ccw":
            return "cw"
        return rotation

    def get_vertical_mirrored_location(self, location: str) -> str:
        return vertical_mirror_map.get(location, location)

    def get_horizontal_mirrored_location(self, location: str) -> str:
        return horizontal_mirror_map.get(location, location)

