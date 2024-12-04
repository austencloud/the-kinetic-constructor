# sequence_rotation_manager.py

from typing import TYPE_CHECKING
from data.constants import *
from data.positions_map import positions_map

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceRotationManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.rotation_steps = 0  # Keep track of rotations
        self.original_sequence_json = None  # Store original sequence
        self.rotation_mapping_90 = {
            "n": "e",
            "ne": "se",
            "e": "s",
            "se": "sw",
            "s": "w",
            "sw": "nw",
            "w": "n",
            "nw": "ne",
        }

    def rotate_current_sequence(self):
        if self.original_sequence_json is None:
            self.original_sequence_json = (
                self.sequence_widget.json_manager.loader_saver.load_current_sequence_json()
            )
        if len(self.original_sequence_json) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            return

        # Update rotation steps
        self.rotation_steps = (self.rotation_steps + 1) % 4

        # Rotate the original sequence
        rotated_sequence_json = self.rotate_sequence(
            self.original_sequence_json, self.rotation_steps
        )
        self.sequence_widget.update_beats_in_place(rotated_sequence_json)
        self.sequence_widget.indicator_label.show_message(
            "Sequence rotated!"
        )

    def rotate_sequence(self, sequence_json, rotation_steps):
        rotated_sequence = []

        # Copy the metadata (first dictionary)
        metadata = sequence_json[0].copy()
        rotated_sequence.append(metadata)

        # Rotate the start position beat
        start_pos_beat = sequence_json[1].copy()
        self._rotate_beat(start_pos_beat, rotation_steps)
        rotated_sequence.append(start_pos_beat)

        # Rotate each beat
        for beat in sequence_json[2:]:
            rotated_beat = beat.copy()
            self._rotate_beat(rotated_beat, rotation_steps)
            rotated_sequence.append(rotated_beat)

        return rotated_sequence

    def _rotate_beat(self, beat, rotation_steps):
        # Rotate blue and red attributes
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat:
                attributes = beat[color]
                # Rotate 'start_loc' and 'end_loc'
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"], rotation_steps
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(
                        attributes["end_loc"], rotation_steps
                    )

        # Recalculate 'start_pos' and 'end_pos' using positions_map
        if "blue_attributes" in beat and "red_attributes" in beat:
            blue_attrs = beat["blue_attributes"]
            red_attrs = beat["red_attributes"]

            if "start_loc" in blue_attrs and "start_loc" in red_attrs:
                beat["start_pos"] = self.get_position_name(
                    blue_attrs["start_loc"], red_attrs["start_loc"]
                )

            if "end_loc" in blue_attrs and "end_loc" in red_attrs:
                beat["end_pos"] = self.get_position_name(
                    blue_attrs["end_loc"], red_attrs["end_loc"]
                )

    def _rotate_location(self, location, rotation_steps):
        if location not in self.rotation_mapping_90:
            return location  # Return as is if not in mapping
        for _ in range(rotation_steps % 4):
            location = self.rotation_mapping_90[location]
        return location

    def get_position_name(self, left_loc, right_loc):
        return positions_map.get((left_loc, right_loc), "unknown")

    def reset_rotation(self):
        self.rotation_steps = 0
        self.original_sequence_json = None
