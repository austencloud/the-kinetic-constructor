from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatFrameUpdater:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame

    def update_beats_from_json(self) -> None:
        current_sequence_json = (
            self.beat_frame.json_manager.loader_saver.load_current_sequence_json()
        )
        # Skip the metadata entry
        sequence_entries = current_sequence_json[1:]

        # Update the start position if necessary
        if sequence_entries and 'sequence_start_position' in sequence_entries[0]:
            self.update_start_pos_from_current_sequence_json(sequence_entries[0])
            beat_entries = sequence_entries[1:]
        else:
            beat_entries = sequence_entries

        for entry in beat_entries:
            if entry.get("is_placeholder", False):
                continue  # Skip placeholders

            beat_num = entry["beat"]
            beat_view = self.beat_frame.get.beat_view_by_number(beat_num)

            if beat_view and beat_view.beat:
                if beat_view.beat.pictograph_dict != entry:
                    beat_view.beat.updater.update_pictograph(entry)
                    QApplication.processEvents()
            else:
                print(
                    f"Beat with number {beat_num} not found in the beat frame. Skipping."
                )
        if beat_entries:
            self.beat_frame.sequence_widget.update_difficulty_label()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.beat_frame.start_pos_view.start_pos.updater.update_pictograph(entry)
