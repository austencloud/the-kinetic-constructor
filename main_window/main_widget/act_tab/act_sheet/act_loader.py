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
            self.act_sheet.act_container.beat_scroll.act_beat_frame.populator.populate_beats(
                act_data["sequences"]
            )
