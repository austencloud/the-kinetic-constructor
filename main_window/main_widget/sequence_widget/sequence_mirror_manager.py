from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from data.positions import mirrored_positions
from data.locations import vertical_loc_mirror_map
from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceMirrorManager:
    vertical_mirror_positions = mirrored_positions["vertical"]

    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_loader = self.sequence_widget.main_widget.json_manager.loader_saver

    def mirror_current_sequence(self):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        mirrored_sequence = self.mirror_sequence()
        self.sequence_widget.beat_frame.updater.update_beats_from(mirrored_sequence)
        self.mirror_option_picker_pictographs()

        self.sequence_widget.indicator_label.show_message("Sequence mirrored!")

        QApplication.restoreOverrideCursor()

    def mirror_option_picker_pictographs(self):
        option_picker = self.sequence_widget.main_widget.construct_tab.option_picker
        for pictograph in option_picker.option_pool:
            new_dict = self._mirror_dict(pictograph.pictograph_dict.copy())
            sequence_so_far = self.json_loader.load_current_sequence_json()
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_dict
            )
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)

            pictograph.updater.update_pictograph(new_dict)

    def check_length(self, current_sequence):
        if len(current_sequence) < 2:
            self.sequence_widget.indicator_label.show_message("No sequence to rotate.")
            QApplication.restoreOverrideCursor()
            return False

    def mirror_sequence(self):
        current_sequence = self.json_loader.load_current_sequence_json()
        metadata = current_sequence[0].copy()

        if self.check_length(current_sequence):
            return
        mirrored_sequence = []
        mirrored_sequence.append(metadata)
        start_pos_beat_dict: dict = (
            self.sequence_widget.beat_frame.start_pos_view.start_pos.pictograph_dict.copy()
        )

        self._mirror_dict(start_pos_beat_dict)
        mirrored_sequence.append(start_pos_beat_dict)

        beat_dicts = self.sequence_widget.beat_frame.get.beat_dicts()
        for beat_dict in beat_dicts:
            mirrored_dict = beat_dict.copy()
            self._mirror_dict(mirrored_dict)
            mirrored_sequence.append(mirrored_dict)
        return mirrored_sequence

    def _mirror_dict(self, pictograph_dict):
        if "start_pos" in pictograph_dict:
            pictograph_dict["start_pos"] = self.vertical_mirror_positions.get(
                pictograph_dict["start_pos"], pictograph_dict["start_pos"]
            )
        if "end_pos" in pictograph_dict:
            pictograph_dict["end_pos"] = self.vertical_mirror_positions.get(
                pictograph_dict["end_pos"], pictograph_dict["end_pos"]
            )

        for color in ["blue_attributes", "red_attributes"]:
            if color in pictograph_dict:
                attributes = pictograph_dict[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = vertical_loc_mirror_map.get(
                        attributes["start_loc"], attributes["start_loc"]
                    )
                if "end_loc" in attributes:
                    attributes["end_loc"] = vertical_loc_mirror_map.get(
                        attributes["end_loc"], attributes["end_loc"]
                    )
                if "prop_rot_dir" in attributes:
                    attributes["prop_rot_dir"] = self.reverse_prop_rot_dir(
                        attributes["prop_rot_dir"]
                    )
        return pictograph_dict

    def reverse_prop_rot_dir(self, prop_rot_dir: str) -> str:
        if prop_rot_dir == "cw":
            return "ccw"
        elif prop_rot_dir == "ccw":
            return "cw"
        else:
            return prop_rot_dir
