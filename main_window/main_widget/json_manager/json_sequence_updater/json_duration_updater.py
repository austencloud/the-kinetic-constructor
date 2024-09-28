from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        BeatView,
    )
    from .json_sequence_updater import JsonSequenceUpdater


class JsonDurationUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater") -> None:
        self.json_manager = json_updater.json_manager

    def update_beat_duration_in_json(
        self, beat_view: "BeatView", new_duration: int
    ) -> None:
        """Main method to update beat duration and adjust subsequent beats."""
        sequence_data = self.json_manager.loader_saver.load_current_sequence_json()

        # Extract metadata and sequence beats
        sequence_metadata, sequence_beats = self._extract_metadata_and_beats(
            sequence_data
        )
        # Split the beats into two parts: before and after the current beat range
        sequence_before, sequence_after = self._split_sequence_by_beat_range(
            sequence_beats, beat_view
        )

        if beat_view.beat.pictograph_dict["duration"] == 1 and new_duration > 1:
            self._add_placeholder_beats(sequence_before, beat_view, new_duration)
        elif beat_view.beat.pictograph_dict["duration"] > 1 and new_duration == 1:
            sequence_after = self._remove_placeholder_beats(sequence_after, beat_view)

        # Adjust the beat data and add placeholders for new duration
        updated_beat_data = self._update_beat_data(beat_view, new_duration)
        sequence_before.append(updated_beat_data)

        # Shift subsequent beats and append them to sequence
        sequence_after = self._shift_subsequent_beats(
            sequence_after, beat_view, new_duration
        )
        sequence_beats = sequence_before + sequence_after

        # Sort the beats and save
        sequence_beats = self._sort_beats(sequence_beats)

        self._fix_beat_counts(sequence_beats)

        self._save_sequence(sequence_metadata, sequence_beats)

    def _fix_beat_counts(self, sequence_beats: list) -> None:
        """Fix the beat counts of the sequence beats."""
        for index, entry in enumerate(sequence_beats):
            if "beat" in entry:
                entry["beat"] = index
            if "parent_beat" in entry:
                parent_beat = entry["parent_beat"]
                for i in range(index, -1, -1):
                    if "letter" in sequence_beats[i]:
                        parent_beat = i
                        break
                entry["parent_beat"] = parent_beat
    def _extract_metadata_and_beats(self, sequence_data: list) -> tuple:
        """Extract metadata and beats from the sequence data."""
        sequence_metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        sequence_beats = sequence_data[1:]
        return sequence_metadata, sequence_beats

    def _split_sequence_by_beat_range(
        self, sequence_beats: list, beat_view: "BeatView"
    ) -> tuple[list, list]:
        """Split the sequence into beats before and after the current beat's range."""
        sequence_before = []
        sequence_after = []

        for entry in sequence_beats:
            if "beat" in entry:
                beat_number = entry["beat"]
                if beat_number < beat_view.number:
                    sequence_before.append(entry)
                elif beat_number > beat_view.number:
                    entry["beat"] += beat_view.beat.duration - 1
                    sequence_after.append(entry)

        return sequence_before, sequence_after

    def _update_beat_data(self, beat_view: "BeatView", new_duration: int) -> dict:
        """Update the main beat data with the new duration."""
        beat_data = beat_view.beat.pictograph_dict
        beat_data["duration"] = new_duration
        beat_data["beat"] = beat_view.number
        return beat_data

    def _add_placeholder_beats(
        self, sequence_beats: list, beat_view: "BeatView", new_duration: int
    ) -> None:
        """Add placeholder beats for the remaining duration."""
        for beat_num in range(beat_view.number + 1, beat_view.number + new_duration):
            placeholder_entry = {
                "beat": beat_num,
                "is_placeholder": True,
                "parent_beat": beat_view.number,
            }
            sequence_beats.append(placeholder_entry)

    def _remove_placeholder_beats(
        self, sequence_beats: list, beat_view: "BeatView"
    ) -> None:
        """Remove placeholder beats for the current beat."""
        sequence_beats = [
            entry
            for entry in sequence_beats
            if entry.get("parent_beat") != beat_view.number
        ]
        return sequence_beats

    def _shift_subsequent_beats(
        self, sequence_after: list, beat_view: "BeatView", new_duration: int
    ) -> list:
        """
        Adjust the beat numbers of subsequent beats to account for the new duration.
        If the duration is increased, subsequent beats should be shifted forward. If decreased, beats shift backward.
        """
        shift_offset = new_duration - beat_view.beat.duration
        for beat in sequence_after:
            beat["beat"] += shift_offset

        return sequence_after

    def _sort_beats(self, sequence_beats: list) -> list:
        """Sort the beats by their beat number."""
        return sorted(sequence_beats, key=lambda entry: entry.get("beat", float("inf")))

    def _save_sequence(self, sequence_metadata: dict, sequence_beats: list) -> None:
        """Save the updated sequence with metadata and beats."""
        sequence_data = [sequence_metadata] + sequence_beats
        self.json_manager.loader_saver.save_current_sequence(sequence_data)
