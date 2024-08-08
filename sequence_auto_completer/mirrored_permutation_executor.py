from typing import TYPE_CHECKING
from sequence_auto_completer.permutation_executor_base import PermutationExecutor

if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completion_manager import (
        SequenceAutoCompletionManager,
    )


class MirroredPermutationExecutor(PermutationExecutor):
    def __init__(
        self,
        autocompleter: "SequenceAutoCompletionManager",
        color_swap_second_half: bool,
    ):
        self.autocompleter = autocompleter
        self.color_swap_second_half = color_swap_second_half

    def create_permutations(self, sequence: list[dict]):
        if not self.can_perform_mirrored_permutation(sequence):
            return

        start_position_entry = (
            sequence.pop(0) if "sequence_start_position" in sequence[0] else None
        )
        sequence_length = len(sequence) - 1
        last_entry = sequence[-1]

        new_entries = []
        next_beat_number = last_entry["beat"] + 1

        for i in range(sequence_length):
            new_entry = self.create_new_mirrored_permutation_entry(
                sequence,
                sequence[i],
                next_beat_number,
                sequence_length * 2,
                self.color_swap_second_half,
            )
            new_entries.append(new_entry)
            sequence.append(new_entry)
            next_beat_number += 1

        if start_position_entry:
            start_position_entry["beat"] = 0
            sequence.insert(0, start_position_entry)

        self.autocompleter.json_manager.loader_saver.save_current_sequence(sequence)
        self.autocompleter.beat_frame.populate_beat_frame_from_json(sequence)

    def can_perform_mirrored_permutation(self, sequence: list[dict]) -> bool:
        return sequence[1]["end_pos"] == sequence[-1]["end_pos"]

    def create_new_mirrored_permutation_entry(
        self,
        sequence: list[dict],
        entry: dict,
        beat: int,
        sequence_length: int,
        color_swap_second_half: bool,
    ) -> dict:
        mid_point = sequence_length // 2
        mirrored_beat_number = (sequence_length - beat) % mid_point
        mirrored_beat = sequence[mirrored_beat_number]
        if color_swap_second_half:
            mirrored_beat = self.swap_colors(mirrored_beat)
        return mirrored_beat

    def swap_colors(self, beat: dict) -> dict:
        beat["blue_attributes"], beat["red_attributes"] = (
            beat["red_attributes"],
            beat["blue_attributes"],
        )
        return beat
