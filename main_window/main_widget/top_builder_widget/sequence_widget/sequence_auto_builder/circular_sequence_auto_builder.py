import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sequence_auto_builder import SequenceAutoBuilder


class CircularSequenceAutoBuilder:
    def __init__(self, auto_builder_dialog: "SequenceAutoBuilder"):
        self.auto_builder_dialog = auto_builder_dialog
        self.sequence_widget = auto_builder_dialog.sequence_widget
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )

    def build_sequence(self, length: int, turn_intensity: int, level: int):
        sequence = []
        word_length = length // 4  # Assuming 4 beats per repetition
        for _ in range(word_length):
            next_pictograph = self._generate_next_pictograph(turn_intensity, level)
            sequence.append(next_pictograph)

        self._apply_strict_rotational_permutations(sequence)
        self._finalize_sequence(sequence)

    def _generate_next_pictograph(self, turn_intensity: int, level: int) -> dict:
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )
        chosen_option = random.choice(options)

        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2:
            chosen_option = self._apply_level_2_constraints(
                chosen_option, turn_intensity
            )
        elif level == 3:
            chosen_option = self._apply_level_3_constraints(
                chosen_option, turn_intensity
            )

        return chosen_option

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        # No turns, only radial orientations
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_constraints(self, pictograph: dict, turn_intensity: int) -> dict:
        # Randomize turns within radial constraints
        pictograph["blue_attributes"]["turns"] = self._randomize_turns(turn_intensity)
        pictograph["red_attributes"]["turns"] = self._randomize_turns(turn_intensity)
        return pictograph

    def _apply_level_3_constraints(self, pictograph: dict, turn_intensity: int) -> dict:
        # Randomize turns with potential non-radial orientations
        pictograph["blue_attributes"]["turns"] = self._randomize_turns(turn_intensity)
        pictograph["red_attributes"]["turns"] = self._randomize_turns(turn_intensity)
        return pictograph

    def _randomize_turns(self, turn_intensity: int) -> int:
        # Turn intensity affects the maximum number of turns
        max_turns = turn_intensity // 25  # Scale to 0-4 max turns
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
