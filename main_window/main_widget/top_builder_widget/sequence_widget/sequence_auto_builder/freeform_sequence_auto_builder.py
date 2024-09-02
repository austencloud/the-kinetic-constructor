from typing import TYPE_CHECKING
import random
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class FreeFormSequenceAutoBuilder:
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
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        self.ori_calculator = (
            self.sequence_widget.main_widget.json_manager.ori_calculator
        )
        self.validation_engine = (
            self.sequence_widget.main_widget.json_manager.validation_engine
        )

    def build_sequence(self):
        length_of_sequence_upon_start = len(self.sequence) - 2
        for _ in range(self.length - length_of_sequence_upon_start):
            next_pictograph = self._generate_next_pictograph()

            # Calculate the correct end orientation after adding turns
            next_pictograph["blue_attributes"]["end_ori"] = (
                self.ori_calculator.calculate_end_orientation(next_pictograph, "blue")
            )
            next_pictograph["red_attributes"]["end_ori"] = (
                self.ori_calculator.calculate_end_orientation(next_pictograph, "red")
            )

            self.sequence.append(next_pictograph)
            self.sequence_widget.populate_sequence(next_pictograph)
            self.validation_engine.validate_last_pictograph()
            self.sequence_widget.top_builder_widget.sequence_builder.option_picker.update_option_picker(
                self.sequence
            )

            # Force the UI to process the updated events and refresh the layout
            # QApplication.processEvents()

    def _generate_next_pictograph(self) -> dict:
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
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
