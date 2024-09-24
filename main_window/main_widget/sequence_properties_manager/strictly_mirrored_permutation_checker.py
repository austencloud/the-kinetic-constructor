from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class StrictlyMirroredPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence[1:]
        length = len(sequence)
        if length < 4:
            return False
        if length % 2 != 0:
            return False

        half_length = length // 2
        first_half = sequence[0:half_length]
        second_half = sequence[half_length:]

        for i in range(half_length):
            first_entry = first_half[i]
            second_entry = second_half[half_length - i - 2]

            if not self._is_mirrored(first_entry, second_entry):
                return False

        return True

    def _is_mirrored(self, first_entry, second_entry) -> bool:
        mirrored_vertical = self._get_mirrored_position(
            first_entry["end_pos"], "vertical"
        )
        mirrored_horizontal = self._get_mirrored_position(
            first_entry["end_pos"], "horizontal"
        )

        return second_entry["end_pos"] in [
            mirrored_vertical,
            mirrored_horizontal,
        ]

    def _get_mirrored_position(self, position, direction):
        mirrored_positions = {
            "vertical": {
                "alpha1": "alpha1",
                "alpha3": "alpha7",
                "alpha5": "alpha5",
                "alpha7": "alpha3",
                "beta1": "beta1",
                "beta3": "beta7",
                "beta5": "beta5",
                "beta7": "beta3",
                "gamma1": "gamma9",
                "gamma3": "gamma15",
                "gamma5": "gamma13",
                "gamma7": "gamma11",
                "gamma9": "gamma1",
                "gamma11": "gamma7",
                "gamma13": "gamma5",
                "gamma15": "gamma3",
            },
            "horizontal": {
                "alpha1": "alpha5",
                "alpha3": "alpha3",
                "alpha5": "alpha1",
                "alpha7": "alpha7",
                "beta1": "beta5",
                "beta3": "beta3",
                "beta5": "beta1",
                "beta7": "beta7",
                "gamma1": "gamma13",
                "gamma3": "gamma11",
                "gamma5": "gamma9",
                "gamma7": "gamma15",
                "gamma9": "gamma5",
                "gamma11": "gamma3",
                "gamma13": "gamma1",
                "gamma15": "gamma7",
            },
        }
        return mirrored_positions[direction][position]
