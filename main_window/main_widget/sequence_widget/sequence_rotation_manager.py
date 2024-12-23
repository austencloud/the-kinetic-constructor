from typing import TYPE_CHECKING
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
        self.metadata = None

    def rotate_beats(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        rotated_sequence = self.rotate_sequence()
        self.sequence_widget.update_beats_in_place(rotated_sequence)
        self.sequence_widget.main_widget.manual_builder.option_picker.update_option_picker()

        self.sequence_widget.indicator_label.show_message("Sequence rotated!")

        QApplication.restoreOverrideCursor()

    def check_length(self):
        if len(self.current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            QApplication.restoreOverrideCursor()
            return False

    def rotate_sequence(self):
        """Rotate the sequence by rotation_steps * 45°."""
        self.current_sequence = self.json_loader.load_current_sequence_json()
        metadata = self.current_sequence[0].copy()
        if self.check_length():
            return
        rotated_sequence = []
        rotated_sequence.append(metadata)
        start_pos_beat_dict: dict = (
            self.sequence_widget.beat_frame.start_pos_view.start_pos.pictograph_dict
        )

        self.rotate_pictograph(start_pos_beat_dict)
        rotated_sequence.append(start_pos_beat_dict)
        beat_dicts = self._get_beat_dicts_from_beat_frame()

        for beat_dict in beat_dicts:
            rotated_beat = beat_dict.copy()
            self.rotate_pictograph(rotated_beat)
            rotated_sequence.append(rotated_beat)

        return rotated_sequence

    def _get_beat_dicts_from_beat_frame(self):
        return [
            beat.beat.get.pictograph_dict()
            for beat in self.sequence_widget.beat_frame.beats
            if beat.is_filled
        ]

    def rotate_pictograph(self, _dict: dict):
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
                _dict["start_pos"] = self.get_position_name(
                    bl["start_loc"], rl["start_loc"]
                )
            if "end_loc" in bl and "end_loc" in rl:
                _dict["end_pos"] = self.get_position_name(bl["end_loc"], rl["end_loc"])

    def _rotate_location(self, location):
        if location not in cw_loc_order:
            return location
        idx = cw_loc_order.index(location)
        new_idx = (idx + 1) % len(cw_loc_order)
        return cw_loc_order[new_idx]

    def get_position_name(self, left_loc, right_loc):
        try:
            return positions_map[(left_loc, right_loc)]
        except KeyError:
            raise ValueError(
                f"Position name not found for locations: {left_loc}, {right_loc}"
            )
