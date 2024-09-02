import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class CircularSequenceAutoBuilder:
    def __init__(
        self,
        sequence_widget: "SequenceWidget",
        length: int,
        turn_intensity: int,
        level: int,
    ):
        self.sequence_widget = sequence_widget
        self.length = length
        self.turn_intensity = turn_intensity
        self.level = level

    def build_sequence(self):
        sequence = []
        word_length = self.length // 4  # Assuming 4 beats per repetition
        for _ in range(word_length):
            next_pictograph = self._generate_next_pictograph()
            sequence.append(next_pictograph)

        self._apply_strict_rotational_permutations(sequence)
        self._finalize_sequence(sequence)

    def _generate_next_pictograph(self) -> dict:
        options = (
            self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_manager.get_next_options()
        )
        chosen_option = random.choice(options)

        if self.level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif self.level == 2:
            chosen_option = self._apply_level_2_constraints(chosen_option)
        elif self.level == 3:
            chosen_option = self._apply_level_3_constraints(chosen_option)

        return chosen_option

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        # No turns, only radial orientations
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_constraints(self, pictograph: dict) -> dict:
        # Randomize turns within radial constraints
        pictograph["blue_attributes"]["turns"] = self._randomize_turns()
        pictograph["red_attributes"]["turns"] = self._randomize_turns()
        return pictograph

    def _apply_level_3_constraints(self, pictograph: dict) -> dict:
        # Randomize turns with potential non-radial orientations
        pictograph["blue_attributes"]["turns"] = self._randomize_turns()
        pictograph["red_attributes"]["turns"] = self._randomize_turns()
        return pictograph

    def _randomize_turns(self) -> int:
        # Turn intensity affects the maximum number of turns
        max_turns = self.turn_intensity // 25  # Scale to 0-4 max turns
        return random.choice([0, 0.5, 1, 1.5, 2][:max_turns])

    def _apply_strict_rotational_permutations(self, sequence: list[dict]) -> None:
        # Logic for applying strict rotational permutations
        for i in range(1, len(sequence)):
            sequence[i]["blue_attributes"] = self._rotate_attributes(
                sequence[i - 1]["blue_attributes"]
            )
            sequence[i]["red_attributes"] = self._rotate_attributes(
                sequence[i - 1]["red_attributes"]
            )

    def _rotate_attributes(self, attributes: dict) -> dict:
        # Logic to rotate attributes based on the current state
        new_attributes = attributes.copy()
        position_map_cw = {"s": "w", "w": "n", "n": "e", "e": "s"}
        position_map_ccw = {"s": "e", "e": "n", "n": "w", "w": "s"}

        new_attributes["start_loc"] = position_map_cw[attributes["start_loc"]]
        new_attributes["end_loc"] = position_map_cw[attributes["end_loc"]]

        # Adjust the orientation as needed
        new_attributes["start_ori"] = (
            self.sequence_widget.main_widget.json_manager.ori_calculator.calculate_end_orientation(
                new_attributes, "blue"
            )
        )
        new_attributes["end_ori"] = new_attributes["start_ori"]

        return new_attributes

    def _finalize_sequence(self, sequence: list[dict]) -> None:
        # Add logic to finalize and display the generated sequence
        self.sequence_widget.beat_frame.populate_beat_frame_from_json(sequence)
        self.sequence_widget.autocompleter.auto_complete_sequence()
