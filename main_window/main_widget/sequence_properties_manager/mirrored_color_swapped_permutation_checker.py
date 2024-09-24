from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )


class MirroredColorSwappedPermutationChecker:
    def __init__(self, manager: "SequencePropertiesManager"):
        self.manager = manager

    def check(self) -> bool:
        sequence = self.manager.sequence[1:]  # Skip metadata
        length = len(sequence)
        if length < 4 or length % 2 != 0:
            return False

        half_length = length // 2
        first_half = sequence[:half_length]
        second_half = sequence[half_length:]

        for i in range(half_length):
            first_entry = first_half[i]
            second_entry = second_half[i]

            if not (self._is_mirrored_and_color_swapped(first_entry, second_entry)):
                return False

        return True

    def _is_mirrored_and_color_swapped(self, first_entry, second_entry) -> bool:
        mirrored_vertical = self._get_mirrored_and_colorswapped_position(
            first_entry["end_pos"], "vertical"
        )
        mirrored_horizontal = self._get_mirrored_and_colorswapped_position(
            first_entry["end_pos"], "horizontal"
        )

        return second_entry["end_pos"] in [
            mirrored_vertical,
            mirrored_horizontal,
        ]

    def _is_color_swapped(self, first_entry, second_entry) -> bool:
        return (
            first_entry["blue_attributes"] == second_entry["red_attributes"]
            and first_entry["red_attributes"] == second_entry["blue_attributes"]
        )

    def _get_mirrored_and_colorswapped_position(self, position, direction):
        mirrored_positions = {
            "vertical": {
                "alpha1": "alpha1",
                "alpha2": "alpha8",
                "alpha3": "alpha7",
                "alpha4": "alpha6",
                "alpha5": "alpha5",
                "alpha6": "alpha4",
                "alpha7": "alpha3",
                "alpha8": "alpha2",
                "beta1": "beta1",
                "beta2": "beta8",
                "beta3": "beta7",
                "beta4": "beta6",
                "beta5": "beta5",
                "beta6": "beta4",
                "beta7": "beta3",
                "beta8": "beta2",
                "gamma1": "gamma9",
                "gamma2": "gamma16",
                "gamma3": "gamma15",
                "gamma4": "gamma14",
                "gamma5": "gamma13",
                "gamma6": "gamma12",
                "gamma7": "gamma11",
                "gamma8": "gamma10",
                "gamma9": "gamma1",
                "gamma10": "gamma8",
                "gamma11": "gamma7",
                "gamma12": "gamma6",
                "gamma13": "gamma5",
                "gamma14": "gamma4",
                "gamma15": "gamma3",
                "gamma16": "gamma2",
            },
            "horizontal": {
                "alpha1": "alpha5",
                "alpha2": "alpha4",
                "alpha3": "alpha3",
                "alpha4": "alpha2",
                "alpha5": "alpha1",
                "alpha6": "alpha8",
                "alpha7": "alpha7",
                "alpha8": "alpha6",
                "beta1": "beta5",
                "beta2": "beta4",
                "beta3": "beta3",
                "beta4": "beta2",
                "beta5": "beta1",
                "beta6": "beta8",
                "beta7": "beta7",
                "beta8": "beta6",
                "gamma1": "gamma13",
                "gamma2": "gamma12",
                "gamma3": "gamma11",
                "gamma4": "gamma10",
                "gamma5": "gamma9",
                "gamma6": "gamma16",
                "gamma7": "gamma15",
                "gamma8": "gamma14",
                "gamma9": "gamma5",
                "gamma10": "gamma4",
                "gamma11": "gamma3",
                "gamma12": "gamma2",
                "gamma13": "gamma1",
                "gamma14": "gamma8",
                "gamma15": "gamma7",
                "gamma16": "gamma6",
            },
        }
        return mirrored_positions[direction][position]
