# sequence_mirror_manager.py

from typing import TYPE_CHECKING
from data.constants import *
from data.positions_map import positions_map
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceMirrorManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        # Define mappings for mirroring positions and locations
        self.vertical_mirror_positions = {
            "alpha1": "alpha1",
            "alpha2": "alpha8",
            "alpha3": "alpha7",
            "alpha4": "alpha6",
            "alpha5": "alpha5",
            "alpha6": "alpha4",
            "alpha7": "alpha3",
            "alpha8": "alpha2",
            "beta1": "beta1",
            "beta2": "beta8",
            "beta3": "beta7",
            "beta4": "beta6",
            "beta5": "beta5",
            "beta6": "beta4",
            "beta7": "beta3",
            "beta8": "beta2",
            "gamma1": "gamma9",
            "gamma2": "gamma16",
            "gamma3": "gamma15",
            "gamma4": "gamma14",
            "gamma5": "gamma13",
            "gamma6": "gamma12",
            "gamma7": "gamma11",
            "gamma8": "gamma10",
            "gamma9": "gamma1",
            "gamma10": "gamma8",
            "gamma11": "gamma7",
            "gamma12": "gamma6",
            "gamma13": "gamma5",
            "gamma14": "gamma4",
            "gamma15": "gamma3",
            "gamma16": "gamma2",
        }

        self.vertical_mirror_locations = {
            "n": "n",
            "e": "w",
            "w": "e",
            "s": "s",
            "ne": "nw",
            "nw": "ne",
            "se": "sw",
            "sw": "se",
        }

    def mirror_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_sequence_json = (
            self.sequence_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence_json) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to mirror.")
            return

        mirrored_sequence_json = self.mirror_sequence(current_sequence_json)
        self.sequence_widget.update_beats_in_place(mirrored_sequence_json)
        self.sequence_widget.indicator_label.show_message("Sequence mirrored!")
        QApplication.restoreOverrideCursor()

    def mirror_sequence(self, sequence_json):
        mirrored_sequence = []

        # Copy the metadata (first dictionary)
        metadata = sequence_json[0].copy()
        mirrored_sequence.append(metadata)

        # Mirror the start position beat
        start_pos_beat = sequence_json[1].copy()
        self._mirror_beat(start_pos_beat)
        mirrored_sequence.append(start_pos_beat)

        # Mirror each beat in the sequence
        for beat in sequence_json[2:]:
            mirrored_beat = beat.copy()
            self._mirror_beat(mirrored_beat)
            mirrored_sequence.append(mirrored_beat)

        return mirrored_sequence

    def _mirror_beat(self, beat):
        # Mirror positions
        if "start_pos" in beat:
            beat["start_pos"] = self.vertical_mirror_positions.get(
                beat["start_pos"], beat["start_pos"]
            )
        if "end_pos" in beat:
            beat["end_pos"] = self.vertical_mirror_positions.get(
                beat["end_pos"], beat["end_pos"]
            )

        # Mirror blue and red attributes
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat:
                attributes = beat[color]
                # Mirror locations
                if "start_loc" in attributes:
                    attributes["start_loc"] = self.vertical_mirror_locations.get(
                        attributes["start_loc"], attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self.vertical_mirror_locations.get(
                        attributes["end_loc"], attributes["end_loc"]
                    )
                # Reverse prop_rot_dir
                if "prop_rot_dir" in attributes:
                    attributes["prop_rot_dir"] = self.reverse_prop_rot_dir(
                        attributes["prop_rot_dir"]
                    )

    def reverse_prop_rot_dir(self, prop_rot_dir):
        if prop_rot_dir == "cw":
            return "ccw"
        elif prop_rot_dir == "ccw":
            return "cw"
        else:
            return prop_rot_dir
