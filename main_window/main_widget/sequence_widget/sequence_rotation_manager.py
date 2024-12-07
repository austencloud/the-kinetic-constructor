# sequence_rotation_manager.py

from typing import TYPE_CHECKING
from data.constants import *
from data.positions_map import positions_map

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceRotationManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.rotation_steps = 0  # An integer in [0..7]; each increment = 45°
        self.original_sequence_json = None

        # Define the order for 45° increments:
        # Index:0 -> N(0°), 1->NE(45°), 2->E(90°), 3->SE(135°), 4->S(180°),
        # 5->SW(225°), 6->W(270°), 7->NW(315°)
        self.loc_order = ["n", "ne", "e", "se", "s", "sw", "w", "nw"]

    def rotate_current_sequence(self):
        # If no original sequence cached, load it now
        if self.original_sequence_json is None:
            self.original_sequence_json = (
                self.sequence_widget.json_manager.loader_saver.load_current_sequence_json()
            )

        if len(self.original_sequence_json) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            return

        # Increment rotation by one step of 45°
        self.rotation_steps = (self.rotation_steps + 1) % 8

        # Rotate the sequence
        rotated_sequence = self.rotate_sequence(self.original_sequence_json, self.rotation_steps)

        # Determine and set the new grid mode based on the rotated sequence
        mode = self._determine_grid_mode(rotated_sequence)
        # IMPORTANT: Set the grid mode before updating beats, so that the correct points exist
        self.sequence_widget.main_widget.manager.set_grid_mode(mode, clear_sequence=False)

        # Now update the beats with the rotated sequence
        self.sequence_widget.update_beats_in_place(rotated_sequence)
        self.sequence_widget.indicator_label.show_message("Sequence rotated!")

    def rotate_sequence(self, sequence_json, rotation_steps):
        """
        Rotate the sequence by rotation_steps * 45° from the original sequence.
        rotation_steps: int in [0..7].
        """
        rotated_sequence = []

        # Copy metadata
        metadata = sequence_json[0].copy()
        rotated_sequence.append(metadata)

        # Rotate start position beat
        start_pos_beat = sequence_json[1].copy()
        self._rotate_beat(start_pos_beat, rotation_steps)
        rotated_sequence.append(start_pos_beat)

        # Rotate each subsequent beat
        for beat in sequence_json[2:]:
            rotated_beat = beat.copy()
            self._rotate_beat(rotated_beat, rotation_steps)
            rotated_sequence.append(rotated_beat)

        return rotated_sequence

    def _rotate_beat(self, beat, rotation_steps):
        # Rotate blue and red attributes by rotation_steps*45°
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat:
                attributes = beat[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(attributes["start_loc"], rotation_steps)
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(attributes["end_loc"], rotation_steps)

        # Recalculate start_pos and end_pos
        if "blue_attributes" in beat and "red_attributes" in beat:
            blue_attrs = beat["blue_attributes"]
            red_attrs = beat["red_attributes"]

            if "start_loc" in blue_attrs and "start_loc" in red_attrs:
                beat["start_pos"] = self.get_position_name(blue_attrs["start_loc"], red_attrs["start_loc"])
            if "end_loc" in blue_attrs and "end_loc" in red_attrs:
                beat["end_pos"] = self.get_position_name(blue_attrs["end_loc"], red_attrs["end_loc"])

    def _rotate_location(self, location, rotation_steps):
        # rotation_steps in [0..7], each step = 45°
        if location not in self.loc_order:
            # If location is unrecognized, return as is. Consider logging a warning if needed.
            return location
        idx = self.loc_order.index(location)
        new_idx = (idx + rotation_steps) % len(self.loc_order)
        return self.loc_order[new_idx]

    def get_position_name(self, left_loc, right_loc):
        return positions_map.get((left_loc, right_loc), "unknown")

    def _determine_grid_mode(self, rotated_sequence):
        """
        Determine if the rotated sequence should be displayed in diamond (cardinal)
        or box (intercardinal) mode based on the end_locs found in the sequence.
        """
        cardinal_set = {"n", "e", "s", "w"}
        intercardinal_set = {"ne", "se", "sw", "nw"}

        # Gather all end_locs from rotated_sequence
        all_locs = []

        # Start position beat end locs
        start_pos_beat = rotated_sequence[1]
        if "blue_attributes" in start_pos_beat and "red_attributes" in start_pos_beat:
            bl = start_pos_beat["blue_attributes"].get("end_loc")
            rl = start_pos_beat["red_attributes"].get("end_loc")
            if bl: all_locs.append(bl)
            if rl: all_locs.append(rl)

        # Other beats
        for beat in rotated_sequence[2:]:
            if "blue_attributes" in beat and "red_attributes" in beat:
                bl = beat["blue_attributes"].get("end_loc")
                rl = beat["red_attributes"].get("end_loc")
                if bl: all_locs.append(bl)
                if rl: all_locs.append(rl)

        # Decide grid mode
        if all(l in cardinal_set for l in all_locs):
            mode = "diamond"
        elif all(l in intercardinal_set for l in all_locs):
            mode = "box"
        else:
            # Mixed, choose majority
            cardinal_count = sum(l in cardinal_set for l in all_locs)
            inter_count = sum(l in intercardinal_set for l in all_locs)
            mode = "diamond" if cardinal_count >= inter_count else "box"

        return mode

    def reset_rotation(self):
        self.rotation_steps = 0
        self.original_sequence_json = None
