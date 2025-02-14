from typing import TYPE_CHECKING

from data.constants import DIAMOND
from .strictly_color_swapped_permutation_checker import (
    StrictlyColorSwappedPermutationChecker,
)
from .mirrored_color_swapped_permutation_checker import (
    MirroredColorSwappedPermutationChecker,
)
from .strictly_mirrored_permutation_checker import StrictlyMirroredPermutationChecker
from .rotated_color_swapped_permutation_checker import (
    RotatedColorSwappedPermutationChecker,
)
from .strictly_rotated_permutation_checker import StrictlyRotatedPermutationChecker

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequencePropertiesManager:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.json_manager = main_widget.json_manager
        self.sequence = None

        # Default properties
        self.properties = {
            "ends_at_start_pos": False,
            "is_permutable": False,
            "is_strictly_rotated_permutation": False,
            "is_strictly_mirrored_permutation": False,
            "is_strictly_colorswapped_permutation": False,
            "is_mirrored_color_swapped_permutation": False,
            "is_rotated_colorswapped_permutation": False,
        }

        # Instantiate the individual checkers
        self.checkers = {
            "is_strictly_rotated_permutation": StrictlyRotatedPermutationChecker(self),
            "is_strictly_mirrored_permutation": StrictlyMirroredPermutationChecker(
                self
            ),
            "is_strictly_colorswapped_permutation": StrictlyColorSwappedPermutationChecker(
                self
            ),
            "is_mirrored_color_swapped_permutation": MirroredColorSwappedPermutationChecker(
                self
            ),
            "is_rotated_colorswapped_permutation": RotatedColorSwappedPermutationChecker(
                self
            ),
        }

    def instantiate_sequence(self, sequence):
        self.sequence = sequence[1:]

    def update_sequence_properties(self):
        sequence = self.json_manager.loader_saver.load_current_sequence()
        if len(sequence) <= 1:
            return

        self.instantiate_sequence(sequence)
        # properties = self.check_all_properties()
        # sequence[0].update(properties)

        self.json_manager.loader_saver.save_current_sequence(sequence)

    def calculate_word(self, sequence):
        if sequence is None or not isinstance(sequence, list):
            sequence = self.json_manager.loader_saver.load_current_sequence()

        if len(sequence) < 2:
            return ""

        word = "".join(
            entry.get("letter", "") for entry in sequence[2:] if "letter" in entry
        )
        return word

    def check_all_properties(self):
        if not self.sequence:
            return self._default_properties()

        # Check basic properties
        self.properties["ends_at_start_pos"] = self._check_ends_at_start_pos()
        self.properties["is_permutable"] = self._check_is_permutable()

        # Check for permutations, starting with strictly rotated
        self.properties["is_strictly_rotated_permutation"] = self.checkers[
            "is_strictly_rotated_permutation"
        ].check()

        if not self.properties["is_strictly_rotated_permutation"]:
            # Cascade checks if not rotated
            for key in [
                "is_strictly_mirrored_permutation",
                "is_strictly_colorswapped_permutation",
                "is_mirrored_color_swapped_permutation",
                "is_rotated_colorswapped_permutation",
            ]:
                self.properties[key] = self.checkers[key].check()

                # Stop further checks if a property is set to True
                if self.properties[key]:
                    break

        return self._gather_properties()

    def _gather_properties(self):
        return {
            "word": self.calculate_word(
                self.json_manager.loader_saver.load_current_sequence()
            ),
            "author": self.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
            "level": self.main_widget.sequence_level_evaluator.get_sequence_difficulty_level(
                self.sequence
            ),
            "grid_mode": self.properties["grid_mode"],
            "is_circular": self.properties["ends_at_start_pos"],
            "is_permutable": self.properties["is_permutable"],
            **{
                key: self.properties[key]
                for key in self.properties
                if key.startswith("is_")
            },
        }

    def _default_properties(self):
        return {
            "word": "",
            "author": self.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
            "level": 0,
            "grid_mode": DIAMOND,
            "is_circular": False,
            "is_permutable": False,
            "is_strictly_rotated_permutation": False,
            "is_strictly_mirrored_permutation": False,
            "is_strictly_colorswapped_permutation": False,
            "is_mirrored_color_swapped_permutation": False,
            "is_rotated_colorswapped_permutation": False,
        }

    def _check_ends_at_start_pos(self) -> bool:
        if self.sequence[-1].get("is_placeholder", False):
            return self.sequence[-2]["end_pos"] == self.sequence[0]["end_pos"]
        else:
            return self.sequence[-1]["end_pos"] == self.sequence[0]["end_pos"]

    def _check_is_permutable(self) -> bool:
        if self.sequence[-1].get("is_placeholder", False):
            return self.sequence[-2]["end_pos"].rstrip("0123456789") == self.sequence[
                0
            ]["end_pos"].rstrip("0123456789")
        else:
            return self.sequence[-1]["end_pos"].rstrip("0123456789") == self.sequence[
                0
            ]["end_pos"].rstrip("0123456789")
