import json
from .motion_orientation_json_calculator import CurrentSequenceJsonOriCalculator
from widgets.pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class CurrentSequenceJsonHandler:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.current_sequence_json = "current_sequence.json"
        self.main_widget = main_widget
        self.ori_calculator = CurrentSequenceJsonOriCalculator(main_widget)
        self.empty_sequence()

    def empty_sequence(self):
        """Empties the sequence file."""
        with open(self.current_sequence_json, "w") as file:
            file.write("[]")

    def set_start_position_data(self, start_pos_graph: Pictograph):
        red_start_ori = start_pos_graph.pictograph_dict["red_start_ori"]
        blue_start_ori = start_pos_graph.pictograph_dict["blue_start_ori"]
        sequence = self.load_sequence()
        start_position_dict = {
            "sequence_start_position": start_pos_graph.end_pos[:-1],
            "red_end_ori": red_start_ori,
            "blue_end_ori": blue_start_ori,
            "end_pos": start_pos_graph.end_pos,
        }

        if sequence and "sequence_start_position" in sequence[0]:
            sequence[0] = start_position_dict
        else:
            sequence.insert(0, start_position_dict)
        self.save_sequence(sequence)

    def load_sequence(self) -> list[dict]:
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
