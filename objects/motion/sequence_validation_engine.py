from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from widgets.current_sequence_json_handler.current_sequence_json_handler import (
        CurrentSequenceJsonHandler,
    )
    from widgets.main_widget.main_widget import MainWidget


class CurrentSequenceJsonValidationEngine:
    def __init__(self, current_sequence_json_handler: "CurrentSequenceJsonHandler"):
        self.json_handler = current_sequence_json_handler
        self.sequence_json = self.json_handler.load_current_sequence_json()

    def validate_and_update_sequence_json(self):
        """Iterates through the sequence, updating start and end orientations to ensure continuity."""
        for i, _ in enumerate(self.sequence_json):
            if i > 0:
                self.update_json_entry_start_orientation(i)
                self.update_json_entry_end_orientation(i)
        self.json_handler.save_sequence(self.sequence_json)

    def update_json_entry_start_orientation(self, index):
        """Updates the start orientation of the current pictograph based on the previous one's end orientation."""
        current_pictograph = self.sequence_json[index]
        previous_pictograph = self.sequence_json[index - 1]
        current_pictograph["red_start_ori"] = previous_pictograph["red_end_ori"]
        current_pictograph["blue_start_ori"] = previous_pictograph["blue_end_ori"]

    def update_json_entry_end_orientation(self, index):
        """Recalculates and updates the end orientation of the current pictograph."""
        pictograph_dict = self.sequence_json[index]
        for color in [Color.RED, Color.BLUE]:
            end_ori = self.json_handler.ori_calculator.calculate_end_orientation(
                pictograph_dict, color
            )
            pictograph_dict[f"{color.value}_end_ori"] = end_ori

    def run(self):
        """Public method to run the sequence validation and update process."""
        self.sequence_json = self.json_handler.load_current_sequence_json()
        self.validate_and_update_sequence_json()
        self.json_handler.save_sequence(self.sequence_json)
