from typing import TYPE_CHECKING
from Enums.Enums import Turns
from data.constants import FLOAT

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget
    from objects.motion.motion import Motion


class JsonTurnsUpdater:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.json_manager = (
            turns_widget.turns_box.adjustment_panel.graph_editor.main_widget.json_manager
        )
        self.json_updater = self.json_manager.updater
        self.beat_frame = (
            turns_widget.turns_box.adjustment_panel.graph_editor.sequence_widget.beat_frame
        )
        self.prop_rot_dir_manager = self.turns_box.prop_rot_dir_button_manager

    def update_turns_in_json(self, motion: "Motion", new_turns: Turns) -> None:
        """Update the turns value in the JSON data."""
        if new_turns == "fl":
            self.json_updater.turns_updater.set_turns_to_fl_from_num_in_json(
                motion, new_turns
            )
        elif motion.motion_type == FLOAT and new_turns != "fl":
            self.json_updater.turns_updater.set_turns_to_num_from_fl_in_json(
                motion, new_turns
            )
        else:
            self.json_updater.turns_updater.set_turns_from_num_to_num_in_json(
                motion, new_turns
            )

    def update_prefloat_values_in_json(self, motion: "Motion", index: int) -> None:
        """Update prefloat values in JSON."""
        self.json_updater.motion_type_updater.update_prefloat_motion_type_in_json(
            index, motion.color, motion.prefloat_motion_type
        )
        self.json_updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            index, motion.color, motion.prefloat_prop_rot_dir
        )
