from typing import TYPE_CHECKING, List, Dict
from sequence_auto_completer.mirrored_permutation_executor import (
    MirroredPermutationExecutor,
)
from sequence_auto_completer.permutation_dialog import PermutationDialog
from sequence_auto_completer.permutation_executor_base import PermutationExecutor
from sequence_auto_completer.rotational_permutation_executor import (
    RotationalPermutationExecuter,
)
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceAutoCompletionManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.beat_frame = sequence_widget.beat_frame
        self.json_manager = self.beat_frame.json_manager

    def perform_auto_completion(self, sequence: list[dict]):
        valid_permutations = self.get_valid_permutations(sequence)
        dialog = PermutationDialog(valid_permutations)
        if dialog.exec():
            option = dialog.get_options()
            executor_options = {
                "rotation": RotationalPermutationExecuter(self),
                "mirror": MirroredPermutationExecutor(
                    self, color_swap_second_half=False
                ),
                "color_swap": MirroredPermutationExecutor(
                    self, color_swap_second_half=True
                ),
            }
            executor: PermutationExecutor = executor_options.get(option)
            if executor:
                executor.create_permutations(sequence)

    def get_valid_permutations(self, sequence: list[dict]) -> Dict[str, bool]:
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        valid_permutations = {
            "rotation": (start_pos, end_pos) in quartered_permutations
            or (start_pos, end_pos) in halved_permutations,
            "mirror": start_pos == end_pos,
            "color_swap": start_pos == end_pos,
        }
        return valid_permutations
