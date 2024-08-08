from typing import TYPE_CHECKING

from sequence_auto_completer.permutation_executor_base import PermutationExecutor


if TYPE_CHECKING:
    from sequence_auto_completer.sequence_auto_completion_manager import (
        SequenceAutoCompletionManager,
    )


class MirroredPermutationExecutor(PermutationExecutor):
    def __init__(
        self, autocompleter: "SequenceAutoCompletionManager", color_swap: bool
    ):
        self.autocompleter = autocompleter
        self.color_swap = color_swap

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
            new_entry = self.autocompleter.rotational_permutationnew_entry_creator.create_new_mirrored_permutation_entryentry(
                sequence,
                sequence[i],
                next_beat_number,
                sequence_length * 2,
                "mirrored",
                self.color_swap,
            )
            new_entries.append(new_entry)
            sequence.append(new_entry)
            next_beat_number += 1

        if start_position_entry:
            start_position_entry["beat"] = 0
            sequence.insert(0, start_position_entry)

        self.autocompleter.json_manager.loader_saver.save_current_sequence(sequence)
        self.autocompleter.beat_frame.populate_beat_frame_from_json(sequence)

    def can_perform_mirrored_permutation(self, sequence):
        return sequence[1]["end_pos"] == sequence[-1]["end_pos"]
