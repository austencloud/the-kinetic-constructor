import json

from Enums.MotionAttributes import Color
from objects.motion.sequence_validation_engine import (
    CurrentSequenceJsonValidationEngine,
)
from widgets.sequence_widget.sequence_beat_frame.beat import BeatView
from .motion_orientation_json_calculator import CurrentSequenceJsonOriCalculator
from widgets.pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.json_manager import JSON_Manager
    from widgets.main_widget.main_widget import MainWidget


class CurrentSequenceJsonHandler:
    def __init__(self, json_manager: "JSON_Manager"):
        self.current_sequence_json = "current_sequence.json"
        self.main_widget = json_manager.main_widget
        self.ori_calculator = CurrentSequenceJsonOriCalculator(self)
        self.validation_engine = CurrentSequenceJsonValidationEngine(self)
        self.empty_sequence()

    def empty_sequence(self):
        """Empties the sequence file."""
        with open(self.current_sequence_json, "w") as file:
            file.write("[]")

    def set_start_position_data(self, start_pos_pictograph: Pictograph):
        red_start_ori = start_pos_pictograph.pictograph_dict["red_start_ori"]
        blue_start_ori = start_pos_pictograph.pictograph_dict["blue_start_ori"]
        sequence = self.load_current_sequence_json()
        start_position_dict = {
            "sequence_start_position": start_pos_pictograph.end_pos[:-1],
            "red_end_ori": red_start_ori,
            "blue_end_ori": blue_start_ori,
            "end_pos": start_pos_pictograph.end_pos,
        }

        if sequence and "sequence_start_position" in sequence[0]:
            sequence[0] = start_position_dict
        else:
            sequence.insert(0, start_position_dict)
        self.save_sequence(sequence)

    def load_current_sequence_json(self) -> list[dict]:
        """Loads the sequence from the JSON file with UTF-8 encoding."""
        try:
            with open(self.current_sequence_json, "r", encoding="utf-8") as file:
                sequence = json.load(file)
            return sequence
        except FileNotFoundError:
            return []

    def save_sequence(self, sequence):
        """Saves the corrected sequence back to the JSON file with UTF-8 encoding."""
        with open(self.current_sequence_json, "w", encoding="utf-8") as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

    def get_red_end_ori(self):
        """Get the red end orientation from the last pictograph in the sequence."""
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[-1]["red_end_ori"]
        return 0

    def get_blue_end_ori(self):
        """Get the blue end orientation from the last pictograph in the sequence."""
        sequence = self.load_current_sequence_json()
        if sequence:
            return sequence[-1]["blue_end_ori"]
        return 0

    def update_current_sequence_file(self):
        temp_filename = "current_sequence.json"
        sequence_data = self.load_current_sequence_json()
        last_beat_view = (
            self.main_widget.sequence_widget.beat_frame.get_last_filled_beat()
        )
        if (
            hasattr(last_beat_view.beat.get, "pictograph_dict")
            and last_beat_view.is_filled
        ):
            last_pictograph_dict = last_beat_view.beat.get.pictograph_dict()
            sequence_data.append(last_pictograph_dict)
        with open(temp_filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

    def clear_current_sequence_file(self):
        with open("current_sequence.json", "w", encoding="utf-8") as file:
            file.write("[]")

    def update_current_sequence_file_with_beat(self, beat_view: BeatView):
        sequence_data = self.load_current_sequence_json()
        sequence_data.append(beat_view.beat.get.pictograph_dict())
        with open("current_sequence.json", "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

    def clear_and_repopulate_the_current_sequence(self):
        self.clear_current_sequence_file()
        beat_frame = self.main_widget.sequence_widget.beat_frame
        beat_views = beat_frame.beat_views
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view)

    def get_index_for_pictograph(self, pictograph: Pictograph):
        sequence = self.load_current_sequence_json()
        for i, entry in enumerate(sequence):
            if entry == pictograph.pictograph_dict:
                return i
        return -1

    def update_turns_in_json_at_index(
        self, index: int, color: Color, turns: Union[int | float]
    ):
        sequence = self.load_current_sequence_json()
        sequence[index][f"{color.value}_turns"] = turns
        end_ori = self.ori_calculator.calculate_end_orientation(sequence[index], color)
        sequence[index][f"{color.value}_end_ori"] = end_ori


        self.save_sequence(sequence)
