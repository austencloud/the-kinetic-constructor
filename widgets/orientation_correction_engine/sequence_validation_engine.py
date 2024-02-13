import json
import logging

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

from widgets.pictograph.pictograph import Pictograph
from .motion_orientation_json_calculator import (
    CurrentSequenceJsonOriCalculator,
)


class SequenceValidationEngine:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.current_sequence_json = "current_sequence.json"
        self.logger = logging.getLogger(__name__)
        self.empty_sequence()

    def empty_sequence(self):
        """Empties the sequence file."""
        with open(self.current_sequence_json, "w") as file:
            file.write("[]")

    def correct_sequence_orientations(self, sequence):
        for i in range(1, len(sequence)):
            prev_pictograph = sequence[i - 1]
            current_pictograph = sequence[i]

            current_pictograph["red_start_ori"] = prev_pictograph["red_end_ori"]
            current_pictograph["blue_start_ori"] = prev_pictograph["blue_end_ori"]

            self.logger.info(
                f"Created start orientations for pictograph {i}: red_start_ori = {prev_pictograph['red_end_ori']}, blue_start_ori = {prev_pictograph['blue_end_ori']}"
            )

            current_pictograph["red_end_ori"] = (
                self.motion_ori_calculator.calculate_end_orientation(
                    current_pictograph, "red"
                )
            )
            current_pictograph["blue_end_ori"] = (
                self.motion_ori_calculator.calculate_end_orientation(
                    current_pictograph, "blue"
                )
            )

            self.logger.info(
                f"Created end orientations for pictograph {i}: red_end_ori = {current_pictograph['red_end_ori']}, blue_end_ori = {current_pictograph['blue_end_ori']}"
            )

            self.logger.info(f"Corrected orientations for pictograph {i}")

        return sequence

    def run_correction_engine(self):
        """Main method to run the correction process."""
        sequence = self.load_sequence()
        if sequence:
            corrected_sequence = self.correct_sequence_orientations(sequence)
            self.save_sequence(corrected_sequence)

    def add_to_sequence(self, pictograph: Pictograph):
        """Adds the pictograph to the sequence."""
        sequence = self.load_sequence()
        sequence.append(pictograph.get.pictograph_dict())
        self.save_sequence(sequence)
        self.logger.info(
            f"Added pictograph to the sequence: {pictograph.get.pictograph_dict()}"
        )
