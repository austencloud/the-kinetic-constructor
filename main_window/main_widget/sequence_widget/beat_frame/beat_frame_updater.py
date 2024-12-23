from typing import TYPE_CHECKING

from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatFrameUpdater:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame

    def update_beats_from_json(self) -> None:
        current_sequence_json = (
            self.beat_frame.json_manager.loader_saver.load_current_sequence_json()
        )
        sequence_entries = current_sequence_json[1:]

        if sequence_entries and "sequence_start_position" in sequence_entries[0]:
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
                # if beat_view.beat.pictograph_dict != entry:
                    beat_view.beat.updater.update_pictograph(entry)
                    beat = beat_view.beat
                    pictograph_index = self.beat_frame.get.index_of_beat(beat_view)
                    sequence_so_far = self.beat_frame.json_manager.loader_saver.load_current_sequence_json()[
                        : pictograph_index + 2
                    ]
                    reversal_info = ReversalDetector.detect_reversal(
                        sequence_so_far, beat.pictograph_dict
                    )
                    beat.blue_reversal = reversal_info["blue_reversal"]
                    beat.red_reversal = reversal_info["red_reversal"]
                    beat.reversal_symbol_manager.update_reversal_symbols()
                    # QApplication.processEvents()
            else:
                print(
                    f"Beat with number {beat_num} not found in the beat frame. Skipping."
                )
        if beat_entries:
            self.beat_frame.sequence_widget.difficulty_label.update_difficulty_label()

    def update_start_pos_from_current_sequence_json(self, entry: dict) -> None:
        entry["red_attributes"]["start_ori"] = entry["red_attributes"]["end_ori"]
        entry["blue_attributes"]["start_ori"] = entry["blue_attributes"]["end_ori"]
        entry["start_pos"] = entry["end_pos"]
        self.beat_frame.start_pos_view.start_pos.updater.update_pictograph(entry)
