from typing import TYPE_CHECKING

from main_window.main_widget.generate_tab.circular.permutation_executors.mirrored_permutation_executor import (
    MirroredPermutationExecutor,
)
from main_window.main_widget.generate_tab.circular.permutation_executors.rotated_permutation_executor import (
    RotatedPermutationExecuter,
)

from .permutation_dialog import PermutationDialog

from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from PyQt6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWorkbench,
    )


class SequenceAutoCompleter:
    def __init__(self, sequence_widget: "SequenceWorkbench"):
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.validation_engine = self.main_widget.json_manager.ori_validation_engine
        self.rotated_permutation_executor = RotatedPermutationExecuter(self)
        self.mirrored_permutation_executor = MirroredPermutationExecutor(self, False)

    def auto_complete_sequence(self):
        sequence = (
            self.sequence_widget.beat_frame.json_manager.loader_saver.load_current_sequence_json()
        )
        self.sequence_properties_manager = self.main_widget.sequence_properties_manager
        self.sequence_properties_manager.instantiate_sequence(sequence)
        properties = self.sequence_properties_manager.check_all_properties()
        is_permutable = properties["is_permutable"]

        if is_permutable:
            self.sequence_widget.autocompleter.perform_auto_completion(sequence)
        else:
            QMessageBox.warning(
                self,
                "Auto-Complete Disabled",
                "The sequence is not permutable and cannot be auto-completed.",
            )

    def perform_auto_completion(self, sequence: list[dict]):
        valid_permutations = self.get_valid_permutations(sequence)
        dialog = PermutationDialog(valid_permutations)
        if dialog.exec():
            option = dialog.get_options()
            if option == "rotation":
                executor = RotatedPermutationExecuter(self)
                executor.create_permutations(sequence)
            elif option == "vertical_mirror":
                executor = MirroredPermutationExecutor(self, False)
                executor.create_permutations(sequence, "vertical")
            elif option == "horizontal_mirror":
                executor = MirroredPermutationExecutor(self, False)
                executor.create_permutations(sequence, "horizontal")

    def get_valid_permutations(self, sequence: list[dict]) -> dict[str, bool]:
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        valid_permutations = {
            "rotation": (start_pos, end_pos) in quartered_permutations
            or (start_pos, end_pos) in halved_permutations,
            "mirror": start_pos == end_pos,
            "color_swap": start_pos == end_pos,
        }
        return valid_permutations
