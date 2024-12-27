# sequence_color_swap_manager.py

from typing import TYPE_CHECKING
from data.positions_map import positions_map
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceColorSwapManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_loader = self.sequence_widget.main_widget.json_manager.loader_saver

    def swap_colors_in_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.sequence_widget.button_panel.toggle_swap_colors_icon()

        swapped_sequence = self.swap_sequence()
        self.sequence_widget.beat_frame.updater.update_beats_from(swapped_sequence)
        self.swap_option_picker_colors()

        self.sequence_widget.indicator_label.show_message("Colors swapped!")

        QApplication.restoreOverrideCursor()

    def swap_option_picker_colors(self):
        option_picker = self.sequence_widget.main_widget.construct_tab.option_picker
        for pictograph in option_picker.option_pool:
            new_dict = self.swap_dict_values(pictograph.pictograph_dict.copy())
            sequence_so_far = self.json_loader.load_current_sequence_json()
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_dict
            )
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)

            pictograph.updater.update_pictograph(new_dict)

    def check_length(self, current_sequence):
        if len(current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message(
                "No sequence to color swap."
            )
            QApplication.restoreOverrideCursor()
            return False

    def swap_sequence(self) -> list[dict]:
        current_sequence = self.json_loader.load_current_sequence_json()
        metadata = current_sequence[0].copy()
        if self.check_length(current_sequence):
            return
        swapped_sequence = []
        swapped_sequence.append(metadata)

        start_pos_beat_dict: dict = (
            self.sequence_widget.beat_frame.start_pos_view.start_pos.pictograph_dict.copy()
        )
        self.swap_dict_values(start_pos_beat_dict)
        swapped_sequence.append(start_pos_beat_dict)

        beat_dicts = self.sequence_widget.beat_frame.get.beat_dicts()
        for beat in beat_dicts:
            swapped_beat = beat.copy()
            self.swap_dict_values(swapped_beat)
            swapped_sequence.append(swapped_beat)
        return swapped_sequence

    def swap_dict_values(self, pictograph_dict):
        pictograph_dict["blue_attributes"], pictograph_dict["red_attributes"] = (
            pictograph_dict["red_attributes"],
            pictograph_dict["blue_attributes"],
        )

        if (
            "start_loc" in pictograph_dict["blue_attributes"]
            and "start_loc" in pictograph_dict["red_attributes"]
        ):
            left_start_loc = pictograph_dict["blue_attributes"]["start_loc"]
            right_start_loc = pictograph_dict["red_attributes"]["start_loc"]
            pictograph_dict["start_pos"] = positions_map.get(
                (left_start_loc, right_start_loc)
            )

        if (
            "end_loc" in pictograph_dict["blue_attributes"]
            and "end_loc" in pictograph_dict["red_attributes"]
        ):
            left_end_loc = pictograph_dict["blue_attributes"]["end_loc"]
            right_end_loc = pictograph_dict["red_attributes"]["end_loc"]
            pictograph_dict["end_pos"] = positions_map.get(
                (left_end_loc, right_end_loc)
            )

        return pictograph_dict
