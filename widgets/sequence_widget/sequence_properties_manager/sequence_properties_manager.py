from typing import TYPE_CHECKING

from widgets.sequence_widget.sequence_properties_manager.color_swapped_permutation_checker import (
    ColorSwappedPermutationChecker,
)
from widgets.sequence_widget.sequence_properties_manager.mirrored_and_color_swapped_permutation_checker import (
    MirroredAndColorSwappedPermutationChecker,
)
from widgets.sequence_widget.sequence_properties_manager.mirrored_permutation_checker import (
    MirroredPermutationChecker,
)
from widgets.sequence_widget.sequence_properties_manager.rotational_and_color_swapped_permutation_checker import (
    RotationalAndColorSwappedPermutationChecker,
)
from widgets.sequence_widget.sequence_properties_manager.rotational_permutation_checker import (
    RotationalPermutationChecker,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequencePropertiesManager:
    def __init__(self, main_widget: "MainWidget", sequence):
        self.main_widget = main_widget
        self.sequence = sequence

        # Default properties
        self.ends_at_start_pos = False
        self.is_permutable = False
        self.is_strictly_rotational_permutation = False
        self.is_strictly_mirrored_permutation = False
        self.is_strictly_colorswapped_permutation = False
        self.is_mirrored_color_swapped_permutation = False
        self.is_rotational_colorswapped_permutation = False

        # Instantiate the individual checkers
        self.rotational_checker = RotationalPermutationChecker(self)
        self.mirrored_checker = MirroredPermutationChecker(self)
        self.color_swapped_checker = ColorSwappedPermutationChecker(self)
        self.mirrored_color_swapped_checker = MirroredAndColorSwappedPermutationChecker(
            self
        )
        self.rotational_color_swapped_checker = (
            RotationalAndColorSwappedPermutationChecker(self)
        )

    def check_all_properties(self):
        if not self.sequence:
            return self._default_properties()

        self.ends_at_start_pos = self._check_ends_at_start_pos()
        self.is_permutable = self._check_is_permutable()
        self.is_strictly_rotational_permutation = self.rotational_checker.check()

        self.is_strictly_mirrored_permutation = self.mirrored_checker.check()
        self.is_strictly_colorswapped_permutation = self.color_swapped_checker.check()
        self.is_mirrored_color_swapped_permutation = (
            self.mirrored_color_swapped_checker.check()
        )
        self.is_rotational_colorswapped_permutation = (
            self.rotational_color_swapped_checker.check()
        )

        return {
            "author": self.main_widget.main_window.settings_manager.users.user_manager.get_current_user(),
            "level": self.main_widget.sequence_level_evaluator.get_sequence_level(
                self.sequence
            ),
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
