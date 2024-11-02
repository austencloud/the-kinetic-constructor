import json
import os
from typing import TYPE_CHECKING
from utilities.path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from .act_sheet import ActSheet


class ActLoader:
    def __init__(self, act_sheet: "ActSheet") -> None:
        self.act_sheet = act_sheet

    def load_act(self, filename="current_act.json") -> None:
        """Load an act from a JSON file in the acts directory."""
        file_path = get_user_editable_resource_path(f"acts/{filename}")
        if not os.path.isfile(file_path):
            print(f"No saved act found at {file_path}")
            return None

        with open(file_path, "r", encoding="utf-8") as f:
            act_data = json.load(f)
            self.populate_act_from_data(act_data)

    def populate_act_from_data(self, act_data):
        """Populate the act based on saved data, using sequence length to determine row spans."""
        beat_frame = self.act_sheet.act_container.beat_scroll.act_beat_frame

        for sequence in act_data["sequences"]:
            start_marker = sequence.get("sequence_start_marker", False)
            sequence_length = sequence.get("sequence_length", 8)
            beats = sequence["beats"]

            # Calculate the number of rows needed to fit this sequence
            num_rows = (sequence_length + self.act_sheet.DEFAULT_COLUMNS - 1) // self.act_sheet.DEFAULT_COLUMNS

            # Populate rows with beats for this sequence
            for row_index in range(num_rows):
                start_idx = row_index * self.act_sheet.DEFAULT_COLUMNS
                end_idx = start_idx + self.act_sheet.DEFAULT_COLUMNS
                beat_data = beats[start_idx:end_idx]

                # Populate each row with the sliced beats
                beat_frame.populator.populate_row_beats(row_index, beat_data)
