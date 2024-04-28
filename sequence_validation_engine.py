from typing import TYPE_CHECKING
from constants import BLUE, RED

if TYPE_CHECKING:
    from widgets.current_sequence_json_handler.current_sequence_json_handler import (
        CurrentSequenceJsonHandler,
    )


class SequenceValidationEngine:
    def __init__(
        self, current_sequence_json_handler: "CurrentSequenceJsonHandler"
    ) -> None:
        self.current_sequence_json_handler = current_sequence_json_handler
        self.ori_calculator = self.current_sequence_json_handler.ori_calculator
        
    def validate_and_update_sequence_json(self,  is_current_sequence=False) -> None:
        """Iterates through the sequence, updating start and end orientations to ensure continuity."""
        for index, _ in enumerate(self.sequence):
            if index > 0:
                self.update_json_entry_start_orientation(index)
                self.update_json_entry_end_orientation(index)
                
        if is_current_sequence:
            self.current_sequence_json_handler.save_current_sequence(self.sequence)

    def update_json_entry_start_orientation(self, index) -> None:
        """Updates the start orientation of the current pictograph based on the previous one's end orientation."""
        current_pictograph = self.sequence[index]
        previous_pictograph = self.sequence[index - 1]
        current_pictograph["red_attributes"]["start_ori"] = previous_pictograph[
            "red_attributes"
        ]["end_ori"]
        current_pictograph["blue_attributes"]["start_ori"] = previous_pictograph[
            "blue_attributes"
        ]["end_ori"]

    def update_json_entry_end_orientation(self, index) -> None:
        """Recalculates and updates the end orientation of the current pictograph."""
        pictograph_dict = self.sequence[index]
        for color in [RED, BLUE]:
            end_ori = self.ori_calculator.calculate_end_orientation(
                pictograph_dict, color
            )
            pictograph_dict[f"{color}_attributes"]["end_ori"] = end_ori
            self.sequence[index] = pictograph_dict
            
    def run(self, is_current_sequence=False) -> None:
        """Public method to run the sequence validation and update process."""
        if is_current_sequence:
            self.sequence = self.current_sequence_json_handler.load_current_sequence_json()
        self.validate_and_update_sequence_json(is_current_sequence)
