from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import BeatView
    from .json_sequence_updater import JsonSequenceUpdater

class JsonDurationUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_beat_duration_in_json(
        self, beat_view: "BeatView", new_duration: int
    ) -> None:
        """
        Update the beat duration in the sequence JSON and adjust subsequent beats.
        """
        sequence_data = self.json_manager.loader_saver.load_current_sequence_json()

        # Filter out old beat data (adjusting for the new duration range)
        sequence_beats = [
            entry
            for entry in sequence_data[1:]
            if "beat" not in entry
            or entry.get("beat") < beat_view.number
            or entry.get("beat") > beat_view.number + beat_view.beat.duration - 1
        ]

        # Update the duration and placeholder entries
        beat_data = beat_view.beat.pictograph_dict
        beat_data["duration"] = new_duration
        beat_data["beat"] = beat_view.number
        sequence_beats.append(beat_data)

        # Add placeholder entries for multi-beat spans
        for beat_num in range(beat_view.number + 1, beat_view.number + new_duration):
            placeholder_entry = {
                "beat": beat_num,
                "is_placeholder": True,
                "parent_beat": beat_view.number,
            }
            sequence_beats.append(placeholder_entry)

        # Sort beats based on their number
        sequence_beats.sort(key=lambda entry: entry.get("beat", float("inf")))

        # Reassemble sequence data with the metadata
        sequence_metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        sequence_data = [sequence_metadata] + sequence_beats

        # Save the updated sequence
        self.json_manager.loader_saver.save_current_sequence(sequence_data)
