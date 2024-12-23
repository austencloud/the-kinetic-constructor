from typing import TYPE_CHECKING
from data.constants import BOX, DIAMOND
from data.positions_map import positions_map
from data.locations import cw_loc_order

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .sequence_widget import SequenceWidget


class SequenceRotationManager:
    """Handles rotating the sequence in 45° increments."""

    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_loader = self.sequence_widget.json_manager.loader_saver

    def rotate_beats(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        rotated_sequence = self.rotate_sequence()
        self.sequence_widget.beat_frame.updater.update_beats_from(rotated_sequence)
        self.rotate_option_picker_pictographs()

        self.sequence_widget.indicator_label.show_message("Sequence rotated!")

        QApplication.restoreOverrideCursor()

    def rotate_option_picker_pictographs(self):
        option_picker = (
            self.sequence_widget.main_widget.build_tab.manual_builder.option_picker
        )
        for pictograph in option_picker.option_pool:
            new_dict = self._rotate_dict(pictograph.pictograph_dict.copy())
            pictograph.updater.update_pictograph(new_dict)

    def check_length(self, current_sequence):
        if len(current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            QApplication.restoreOverrideCursor()
            return False

    def rotate_sequence(self):
        """Rotate the sequence by rotation_steps * 45°."""
        current_sequence = self.json_loader.load_current_sequence_json()
        metadata = current_sequence[0].copy()

        self.swap_grid_mode(metadata)

        if self.check_length(current_sequence):
            return
        rotated_sequence = []
        rotated_sequence.append(metadata)
        start_pos_beat_dict: dict = (
            self.sequence_widget.beat_frame.start_pos_view.start_pos.pictograph_dict.copy()
        )

        self._rotate_dict(start_pos_beat_dict)
        rotated_sequence.append(start_pos_beat_dict)

        beat_dicts = self.sequence_widget.beat_frame.get.beat_dicts()
        for beat_dict in beat_dicts:
            rotated_dict = beat_dict.copy()
            self._rotate_dict(rotated_dict)
            rotated_sequence.append(rotated_dict)
        return rotated_sequence

    def swap_grid_mode(self, metadata):
        metadata["grid_mode"] = BOX if metadata["grid_mode"] == DIAMOND else DIAMOND

    def _rotate_dict(self, _dict: dict):
        for color in ["blue_attributes", "red_attributes"]:
            if color in _dict:
                attributes = _dict[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(attributes["end_loc"])

        if "blue_attributes" in _dict and "red_attributes" in _dict:
            bl = _dict["blue_attributes"]
            rl = _dict["red_attributes"]
            if "start_loc" in bl and "start_loc" in rl:
                _dict["start_pos"] = positions_map[(bl["start_loc"], rl["start_loc"])]
            if "end_loc" in bl and "end_loc" in rl:
                _dict["end_pos"] = positions_map[(bl["end_loc"], rl["end_loc"])]

        return _dict

    def _rotate_location(self, location):
        if location not in cw_loc_order:
            return location
        idx = cw_loc_order.index(location)
        new_idx = (idx + 1) % len(cw_loc_order)
        return cw_loc_order[new_idx]
