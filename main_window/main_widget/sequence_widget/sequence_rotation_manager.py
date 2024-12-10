# sequence_rotation_manager.py

from typing import TYPE_CHECKING
from data.constants import *
from data.positions_map import positions_map
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceRotationManager:
    """Handles rotating the sequence in 45° increments and updates grid mode."""

    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.rotation_steps = 0
        self.original_sequence_json = None
        self.loc_order = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

    def rotate_current_sequence(self):
        """Rotate the current sequence by 45° increments and update grid mode."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if self.original_sequence_json is None:
            self.original_sequence_json = (
                self.sequence_widget.json_manager.loader_saver.load_current_sequence_json()
            )

        if len(self.original_sequence_json) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            return

        self.rotation_steps = (self.rotation_steps + 1) % 8
        rotated_sequence = self.rotate_sequence(
            self.original_sequence_json, self.rotation_steps
        )

        self.update_grid_mode(rotated_sequence)
        self.sequence_widget.update_beats_in_place(rotated_sequence)
        self.sequence_widget.indicator_label.show_message("Sequence rotated!")
        QApplication.restoreOverrideCursor()

    def update_grid_mode(self, rotated_sequence):
        mode = self._determine_grid_mode(rotated_sequence)
        rotated_sequence[0]["grid_mode"] = mode
        grid_mode_selector = (
            self.sequence_widget.main_widget.menu_bar_widget.grid_mode_selector
        )
        grid_mode_selector.label.setText(mode.capitalize())
        grid_mode_selector.settings_manager.global_settings.set_grid_mode(mode.lower())
        self.sequence_widget.main_widget.manager.set_grid_mode(
            mode, clear_sequence=False
        )

    def rotate_sequence(self, sequence_json, rotation_steps):
        """Rotate the sequence by rotation_steps * 45°."""
        rotated_sequence = []
        metadata = sequence_json[0].copy()
        rotated_sequence.append(metadata)
        start_pos_beat = sequence_json[1].copy()
        self._rotate_beat(start_pos_beat, rotation_steps)
        rotated_sequence.append(start_pos_beat)
        for beat in sequence_json[2:]:
            rotated_beat = beat.copy()
            self._rotate_beat(rotated_beat, rotation_steps)
            rotated_sequence.append(rotated_beat)
        return rotated_sequence

    def _rotate_beat(self, beat, rotation_steps):
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat:
                attributes = beat[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"], rotation_steps
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(
                        attributes["end_loc"], rotation_steps
                    )

        if "blue_attributes" in beat and "red_attributes" in beat:
            bl = beat["blue_attributes"]
            rl = beat["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                beat["start_pos"] = self.get_position_name(
                    bl["start_loc"], rl["start_loc"]
                )
            if "end_loc" in bl and "end_loc" in rl:
                beat["end_pos"] = self.get_position_name(bl["end_loc"], rl["end_loc"])

    def _rotate_location(self, location, rotation_steps):
        if location not in self.loc_order:
            return location
        idx = self.loc_order.index(location)
        new_idx = (idx + rotation_steps) % len(self.loc_order)
        return self.loc_order[new_idx]

    def get_position_name(self, left_loc, right_loc):
        try:
            return positions_map[(left_loc, right_loc)]
        except KeyError:
            raise ValueError(
                f"Position name not found for locations: {left_loc}, {right_loc}"
            )

    def _determine_grid_mode(self, rotated_sequence):
        """Return 'diamond' or 'box' based on the final orientation of all end_locs."""
        cardinal_set = {"n", "e", "s", "w"}
        intercardinal_set = {"ne", "se", "sw", "nw"}
        all_locs = []

        start_pos_beat = rotated_sequence[1]
        if "blue_attributes" in start_pos_beat and "red_attributes" in start_pos_beat:
            bl = start_pos_beat["blue_attributes"].get("end_loc")
            rl = start_pos_beat["red_attributes"].get("end_loc")
            if bl:
                all_locs.append(bl)
            if rl:
                all_locs.append(rl)

        for beat in rotated_sequence[2:]:
            if "blue_attributes" in beat and "red_attributes" in beat:
                bl = beat["blue_attributes"].get("end_loc")
                rl = beat["red_attributes"].get("end_loc")
                if bl:
                    all_locs.append(bl)
                if rl:
                    all_locs.append(rl)

        if all(l in cardinal_set for l in all_locs):
            mode = "diamond"
        elif all(l in intercardinal_set for l in all_locs):
            mode = "box"
        else:
            cardinal_count = sum(l in cardinal_set for l in all_locs)
            inter_count = sum(l in intercardinal_set for l in all_locs)
            mode = "diamond" if cardinal_count >= inter_count else "box"

        return mode

    def reset_rotation(self):
        """Reset rotation to original state."""
        self.rotation_steps = 0
        self.original_sequence_json = None
