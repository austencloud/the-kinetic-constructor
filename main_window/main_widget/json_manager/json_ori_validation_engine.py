from typing import TYPE_CHECKING
from data.constants import BLUE, RED

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonOrientationValidationEngine:
    def __init__(self, json_manager: "JsonManager") -> None:
        self.json_manager = json_manager
        self.ori_calculator = self.json_manager.ori_calculator

    def validate_and_update_json_orientations(self, is_current_sequence=False) -> None:
        """Iterates through the sequence, updating start and end orientations to ensure continuity."""
        for index, _ in enumerate(self.sequence):
            if index > 1:
                if self.sequence[index].get("is_placeholder", False):
                    continue
                self.update_json_entry_start_orientation(index)
                self.update_json_entry_end_orientation(index)

        if is_current_sequence:
            self.json_manager.loader_saver.save_current_sequence(self.sequence)

    def validate_single_pictograph(
        self, pictograph: dict, previous_pictograph: dict
    ) -> dict:
        """
        Validates and updates the start and end orientations of a single pictograph.
        """
        # Update start orientation based on the previous pictograph
        pictograph["red_attributes"]["start_ori"] = previous_pictograph[
            "red_attributes"
        ]["end_ori"]
        pictograph["blue_attributes"]["start_ori"] = previous_pictograph[
            "blue_attributes"
        ]["end_ori"]

        # Recalculate the end orientation
        for color in ["red", "blue"]:
            pictograph[f"{color}_attributes"]["end_ori"] = (
                self.ori_calculator.calculate_end_ori(pictograph, color)
            )

        return pictograph

    def update_json_entry_start_orientation(self, index) -> None:
        """Updates the start orientation of the current pictograph based on the previous one's end orientation."""
        current_pictograph = self.sequence[index]
        previous_pictograph = self.get_previous_pictograph(index)
        current_pictograph["red_attributes"]["start_ori"] = previous_pictograph[
            "red_attributes"
        ]["end_ori"]
        current_pictograph["blue_attributes"]["start_ori"] = previous_pictograph[
            "blue_attributes"
        ]["end_ori"]

    def get_previous_pictograph(self, index) -> dict:
        """Returns the previous pictograph in the sequence."""
        if self.sequence[index - 1].get("is_placeholder", False):
            if self.sequence[index - 2].get("is_placeholder", False):
                return self.sequence[index - 3]
            return self.sequence[index - 2]
        return self.sequence[index - 1]

    def update_json_entry_end_orientation(self, index) -> None:
        """Recalculates and updates the end orientation of the current pictograph."""
        pictograph_dict = self.sequence[index]
        for color in [RED, BLUE]:
            end_ori = self.ori_calculator.calculate_end_ori(pictograph_dict, color)
            pictograph_dict[f"{color}_attributes"]["end_ori"] = end_ori
            self.sequence[index] = pictograph_dict

    def run(self, is_current_sequence=False) -> None:
        """Public method to run the sequence validation and update process."""
        if is_current_sequence:
            self.sequence = self.json_manager.loader_saver.load_current_sequence_json()
        self.validate_and_update_json_orientations(is_current_sequence)

    def validate_last_pictograph(self) -> None:
        """Validates the most recently added pictograph dict."""
        self.sequence = self.json_manager.loader_saver.load_current_sequence_json()
        self.update_json_entry_start_orientation(-1)
        self.update_json_entry_end_orientation(-1)
        self.json_manager.loader_saver.save_current_sequence(self.sequence)
