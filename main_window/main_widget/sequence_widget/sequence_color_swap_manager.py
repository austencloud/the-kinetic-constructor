# sequence_color_swap_manager.py

from typing import TYPE_CHECKING
from data.constants import *
from data.positions_map import positions_map
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceColorSwapManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.positions_map = positions_map  # Assuming positions_map is imported

    def swap_colors_in_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        current_sequence_json = (
            self.sequence_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        if len(current_sequence_json) < 2:
            self.sequence_widget.indicator_label.show_message(
                "No sequence to swap colors."
            )
            QApplication.restoreOverrideCursor()
            return

        self.sequence_widget.button_panel.toggle_swap_colors_icon()
        swapped_sequence_json = self.swap_colors(current_sequence_json)
        self.sequence_widget.update_beats_in_place(swapped_sequence_json)
        self.sequence_widget.indicator_label.show_message("Colors swapped!")
        QApplication.restoreOverrideCursor()

    def swap_colors(self, sequence_json: list[dict]) -> list[dict]:
        swapped_sequence = []

        # Copy the metadata (first dictionary)
        metadata = sequence_json[0].copy()
        swapped_sequence.append(metadata)

        # Swap colors in the start position beat
        if len(sequence_json) > 1:
            start_pos_beat = sequence_json[1].copy()
            self._swap_beat(start_pos_beat)
            swapped_sequence.append(start_pos_beat)
        else:
            return sequence_json  # Return the original sequence if no start position

        # Swap colors in each beat
        for beat in sequence_json[2:]:
            swapped_beat = beat.copy()
            self._swap_beat(swapped_beat)
            swapped_sequence.append(swapped_beat)

        return swapped_sequence

    def _swap_beat(self, beat):
        # Swap blue and red attributes
        beat["blue_attributes"], beat["red_attributes"] = (
            beat["red_attributes"],
            beat["blue_attributes"],
        )

        # Recalculate 'start_pos' and 'end_pos' based on swapped attributes
        # For 'start_pos'
        if (
            "start_loc" in beat["blue_attributes"]
            and "start_loc" in beat["red_attributes"]
        ):
            left_start_loc = beat["blue_attributes"]["start_loc"]
            right_start_loc = beat["red_attributes"]["start_loc"]
            beat["start_pos"] = self.get_position_name(left_start_loc, right_start_loc)

        # For 'end_pos'
        if "end_loc" in beat["blue_attributes"] and "end_loc" in beat["red_attributes"]:
            left_end_loc = beat["blue_attributes"]["end_loc"]
            right_end_loc = beat["red_attributes"]["end_loc"]
            beat["end_pos"] = self.get_position_name(left_end_loc, right_end_loc)

    def get_position_name(self, left_loc, right_loc):
        return self.positions_map.get((left_loc, right_loc), "unknown")
