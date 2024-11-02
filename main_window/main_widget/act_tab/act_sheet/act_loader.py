# act_loader.py

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
        file_path = get_user_editable_resource_path(filename)
        if not os.path.isfile(file_path):
            print(f"No saved act found at {file_path}")
            return None

        with open(file_path, "r") as f:
            act_data = json.load(f)
            self.populate_act_from_data(act_data)

    def populate_act_from_data(self, act_data):
        """Populate the act with multi-row sequences based on saved data."""
        for sequence in act_data["sequences"]:
            rows_to_populate = sequence["sequence_rows"]
            for row_index, row_data in enumerate(rows_to_populate):
                beat_data = sequence["beats"][row_index * 8 : (row_index + 1) * 8]
                self.act_sheet.act_container.beat_scroll.act_beat_frame.populator.populate_row_beats(row_data, beat_data)
