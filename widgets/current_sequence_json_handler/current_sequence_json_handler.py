import json

from widgets.sequence_widget.sequence_beat_frame.beat import BeatView
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

    def set_start_position_data(self, start_pos_pictograph: Pictograph):
        red_start_ori = start_pos_pictograph.pictograph_dict["red_start_ori"]
        blue_start_ori = start_pos_pictograph.pictograph_dict["blue_start_ori"]
        sequence = self.load_sequence()
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

    def update_current_sequence_file(self):
        temp_filename = "current_sequence.json"
        sequence_data = self.load_sequence()
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
        sequence_data = self.load_sequence()
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
