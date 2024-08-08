from typing import TYPE_CHECKING


from sequence_auto_completer.mirrored_permutation_executor import MirroredPermutationExecutor
from sequence_auto_completer.permutation_dialog import PermutationDialog
from sequence_auto_completer.permutation_executor_base import PermutationExecutor
from sequence_auto_completer.rotational_permutation_executor import RotationalPermutationExecuter

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceAutoCompletionManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.beat_frame = sequence_widget.beat_frame
        self.json_manager = self.beat_frame.json_manager

        self.rotational_permutation_executor = RotationalPermutationExecuter(self)
        self.mirrored_permutation_executor = MirroredPermutationExecutor(self, False)

    def perform_auto_completion(self, sequence: list[dict]):
        dialog = PermutationDialog()
        if dialog.exec():
            option = dialog.get_options()
            executor_options = {
                "rotation": RotationalPermutationExecuter(self),
                "mirror": MirroredPermutationExecutor(self, color_swap=False),
                "color_swap": MirroredPermutationExecutor(self, color_swap=True)
            }
            executor: PermutationExecutor = executor_options.get(option)
            executor.create_permutations(sequence)
