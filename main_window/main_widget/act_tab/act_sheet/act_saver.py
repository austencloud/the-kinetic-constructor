import json
import os
from typing import TYPE_CHECKING

from utilities.path_helpers import get_user_editable_resource_path

if TYPE_CHECKING:
    from .act_sheet import ActSheet


class ActSaver:
    def __init__(self, act_sheet: "ActSheet"):
        self.act_sheet = act_sheet

    def save_act(self, filename="current_act.json"):
        """Save the current act to a JSON file in the acts directory."""
        sequences = self.act_sheet.sequence_collector.collect_sequences()
        act_data = {
            "title": self.act_sheet.act_header.get_title(),
            "prop_type": self.act_sheet.main_widget.prop_type.name,
            "grid_mode": self.act_sheet.main_widget.settings_manager.global_settings.get_grid_mode(),
            "sequences": sequences,
        }
        acts_dir = get_user_editable_resource_path("acts")
        os.makedirs(acts_dir, exist_ok=True)
        file_path = os.path.join(acts_dir, filename)

        with open(file_path, "w") as f:
            json.dump(act_data, f, indent=4)