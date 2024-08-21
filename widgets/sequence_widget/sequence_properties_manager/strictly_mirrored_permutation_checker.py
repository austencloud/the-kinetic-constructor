from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_properties_manager.sequence_properties_manager import (
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
        return mirrored_positions[direction][position]
