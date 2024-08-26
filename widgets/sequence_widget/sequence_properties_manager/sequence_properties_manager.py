from typing import TYPE_CHECKING

from widgets.word_simplifier import WordSimplifier
from .strictly_color_swapped_permutation_checker import (
    StrictlyColorSwappedPermutationChecker,
)
from .mirrored_color_swapped_permutation_checker import (
    MirroredColorSwappedPermutationChecker,
)
from .strictly_mirrored_permutation_checker import StrictlyMirroredPermutationChecker
from .rotational_color_swapped_permutation_checker import (
    RotationalColorSwappedPermutationChecker,
)
from .strictly_rotational_permutation_checker import (
    StrictlyRotationalPermutationChecker,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequencePropertiesManager:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.sequence = None
        # Default properties
        self.ends_at_start_pos = False
        self.is_permutable = False
        self.is_strictly_rotational_permutation = False
        self.is_strictly_mirrored_permutation = False
        self.is_strictly_colorswapped_permutation = False
        self.is_mirrored_color_swapped_permutation = False
        self.is_rotational_colorswapped_permutation = False

        # Instantiate the individual checkers
        self.rotational_checker = StrictlyRotationalPermutationChecker(self)
        self.mirrored_checker = StrictlyMirroredPermutationChecker(self)
        self.color_swapped_checker = StrictlyColorSwappedPermutationChecker(self)
        self.mirrored_color_swapped_checker = MirroredColorSwappedPermutationChecker(
            self
        )
        self.rotational_color_swapped_checker = (
            RotationalColorSwappedPermutationChecker(self)
        )

    def instantiate_sequence(self, sequence):
        self.sequence = sequence[1:]

    def calculate_word(self) -> str:
        # Concatenate all letters in the sequence
        word = ''.join(entry['letter'] for entry in self.sequence[1:])
        # Simplify the word using the WordSimplifier
        simplified_word = WordSimplifier.simplify_repeated_word(word)
        return simplified_word

    def check_all_properties(self):
        if not self.sequence:
            return self._default_properties()

        self.ends_at_start_pos = self._check_ends_at_start_pos()
        self.is_permutable = self._check_is_permutable()

        # Check for strictly rotational permutation first
        self.is_strictly_rotational_permutation = self.rotational_checker.check()

        if not self.is_strictly_rotational_permutation:
            # If not rotational, check for strictly mirrored permutation
            self.is_strictly_mirrored_permutation = self.mirrored_checker.check()

            if not self.is_strictly_mirrored_permutation:
                # If not mirrored, check for strictly color swapped permutation
                self.is_strictly_colorswapped_permutation = self.color_swapped_checker.check()

                if not self.is_strictly_colorswapped_permutation:
                    # If not strictly color swapped, check for mirrored color swapped permutation
                    self.is_mirrored_color_swapped_permutation = self.mirrored_color_swapped_checker.check()

                    if not self.is_mirrored_color_swapped_permutation:
                        # If not mirrored color swapped, check for rotational color swapped permutation
                        self.is_rotational_colorswapped_permutation = self.rotational_color_swapped_checker.check()
                    else:
                        self.is_rotational_colorswapped_permutation = False
                else:
                    self.is_mirrored_color_swapped_permutation = False
                    self.is_rotational_colorswapped_permutation = False
            else:
                self.is_strictly_colorswapped_permutation = False
                self.is_mirrored_color_swapped_permutation = False
                self.is_rotational_colorswapped_permutation = False
        else:
            # If it's strictly rotational, all other permutations are false
            self.is_strictly_mirrored_permutation = False
            self.is_strictly_colorswapped_permutation = False
            self.is_mirrored_color_swapped_permutation = False
            self.is_rotational_colorswapped_permutation = False

        return {
            "word": self.calculate_word(),
            "author": self.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
            "level": self.main_widget.sequence_level_evaluator.get_sequence_level(self.sequence),
            "is_circular": self.ends_at_start_pos,
            "is_permutable": self.is_permutable,
            "is_strictly_rotational_permutation": self.is_strictly_rotational_permutation,
            "is_strictly_mirrored_permutation": self.is_strictly_mirrored_permutation,
            "is_strictly_colorswapped_permutation": self.is_strictly_colorswapped_permutation,
            "is_mirrored_color_swapped_permutation": self.is_mirrored_color_swapped_permutation,
            "is_rotational_colorswapped_permutation": self.is_rotational_colorswapped_permutation,
        }

    def _default_properties(self):
        return {
            "word": "",
            "author": self.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
            "level": 0,
            "is_circular": False,
            "is_permutable": False,
            "is_strictly_rotational_permutation": False,
            "is_strictly_mirrored_permutation": False,
            "is_strictly_colorswapped_permutation": False,
            "is_mirrored_color_swapped_permutation": False,
            "is_rotational_colorswapped_permutation": False,
        }

    def _check_ends_at_start_pos(self) -> bool:
        start_position = self.sequence[0]["end_pos"]
        current_position = self.sequence[-1]["end_pos"]
        return current_position == start_position

    def _check_is_permutable(self) -> bool:
        start_position = self.sequence[0]["end_pos"].rstrip("0123456789")
        current_position = self.sequence[-1]["end_pos"].rstrip("0123456789")
        return current_position == start_position
