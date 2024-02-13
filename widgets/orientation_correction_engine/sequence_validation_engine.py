import json
import logging

from widgets.pictograph.pictograph import Pictograph
from .motion_orientation_json_calculator import (
    MotionOrientationJsonCalculator,
)


class SequenceValidationEngine:
    def __init__(
        self, sequence_file="current_sequence.json", motion_ori_calculator=None
    ):
        self.sequence_file = sequence_file
        self.motion_ori_calculator = motion_ori_calculator
        self.logger = logging.getLogger(__name__)
        self.empty_sequence()

    def empty_sequence(self):
        """Empties the sequence file."""
        with open(self.sequence_file, "w") as file:
            file.write("[]")

    def load_sequence(self):
        """Loads the sequence from the JSON file with UTF-8 encoding."""
        try:
            with open(self.sequence_file, "r", encoding="utf-8") as file:
                sequence = json.load(file)
            return sequence
        except FileNotFoundError:
            return []

    def save_sequence(self, sequence):
        """Saves the corrected sequence back to the JSON file with UTF-8 encoding."""
        with open(self.sequence_file, "w", encoding="utf-8") as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

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
                MotionOrientationJsonCalculator.calculate_end_orientation(
                    current_pictograph, "red"
                )
            )
            current_pictograph["blue_end_ori"] = (
                MotionOrientationJsonCalculator.calculate_end_orientation(
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

    def get_red_end_ori(self):
        """Get the red end orientation from the last pictograph in the sequence."""
        sequence = self.load_sequence()
        if sequence:
            return sequence[-1]["red_end_ori"]
        return 0

    def get_blue_end_ori(self):
        """Get the blue end orientation from the last pictograph in the sequence."""
        sequence = self.load_sequence()
        if sequence:
            return sequence[-1]["blue_end_ori"]
        return 0

    def add_to_sequence(self, pictograph: Pictograph):
        """Adds the pictograph to the sequence."""
        sequence = self.load_sequence()
        sequence.append(pictograph.get.pictograph_dict())
        self.save_sequence(sequence)
        self.logger.info(
            f"Added pictograph to the sequence: {pictograph.get.pictograph_dict()}"
        )

    def set_start_position(self, start_pos_graph: Pictograph):
        red_start_ori = start_pos_graph.pictograph_dict["red_start_ori"]
        blue_start_ori = start_pos_graph.pictograph_dict["blue_start_ori"]
        sequence = self.load_sequence()
        start_position_dict = {
            "sequence_start_position": start_pos_graph.end_pos,
            "red_end_ori": red_start_ori,
            "blue_end_ori": blue_start_ori,
            "end_pos": start_pos_graph.end_pos,
        }
        # Check if the sequence already has a start position dictionary and update it,
        # otherwise, insert it at the beginning
        if sequence and "sequence_start_position" in sequence[0]:
            sequence[0] = start_position_dict
        else:
            sequence.insert(0, start_position_dict)
        self.save_sequence(sequence)
