from typing import List, Dict, Tuple, TYPE_CHECKING

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
        """Update beat duration and adjust subsequent beats in the sequence."""
        sequence_data = self._load_sequence_data()
        sequence_metadata, sequence_beats = self._extract_metadata_and_beats(
            sequence_data
        )

        sequence_before, current_beat_data, sequence_after = self._split_sequence(
            sequence_beats, beat_view
        )

        updated_beat_data = self._update_beat_data(current_beat_data, new_duration)
        sequence_before.append(updated_beat_data)

        if new_duration > 1:
            placeholders = self._generate_placeholders(beat_view.number, new_duration)
            sequence_before.extend(placeholders)
            sequence_after = self._shift_beats(sequence_after, shift=new_duration - 1)
        elif new_duration < current_beat_data.get("duration", 1):
            sequence_after = self._shift_beats(
                sequence_after, shift=new_duration - current_beat_data["duration"]
            )
            sequence_after = self._remove_placeholders(sequence_after, beat_view.number)

        sequence_beats = sequence_before + sequence_after
        self._finalize_and_save_sequence(sequence_metadata, sequence_beats)

    # --- Helper Methods ---

    def _load_sequence_data(self) -> List[Dict]:
        """Load the current sequence JSON data."""
        return self.json_manager.loader_saver.load_current_sequence_json()

    def _extract_metadata_and_beats(
        self, sequence_data: List[Dict]
    ) -> Tuple[Dict, List[Dict]]:
        """Separate metadata from the sequence beats."""
        metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        beats = sequence_data[1:]
        return metadata, beats

    def _split_sequence(
        self, sequence_beats: List[Dict], beat_view: "BeatView"
    ) -> Tuple[List[Dict], Dict, List[Dict]]:
        """Split the sequence into parts before, at, and after the current beat."""
        before = []
        after = []
        current_beat_data = None

        for entry in sequence_beats:
            beat_num = entry.get("beat")
            if beat_num < beat_view.number:
                before.append(entry)
            elif beat_num == beat_view.number:
                current_beat_data = entry
            elif beat_num > beat_view.number:
                after.append(entry)

        return before, current_beat_data, after

    def _update_beat_data(self, beat_data: Dict, new_duration: int) -> Dict:
        """Update the beat's duration."""
        updated_data = beat_data.copy()
        updated_data["duration"] = new_duration
        return updated_data

    def _generate_placeholders(self, parent_beat_num: int, duration: int) -> List[Dict]:
        """Create placeholder beats for the extended duration."""
        placeholders = [
            {
                "beat": parent_beat_num + offset,
                "is_placeholder": True,
                "parent_beat": parent_beat_num,
            }
            for offset in range(1, duration)
        ]
        return placeholders

    def _shift_beats(self, beats: List[Dict], shift: int) -> List[Dict]:
        """Shift beat numbers by a specified amount."""
        if shift == 0:
            return beats

        for beat in beats:
            beat["beat"] += shift
            if "parent_beat" in beat:
                beat["parent_beat"] += shift
        return beats

    def _remove_placeholders(
        self, beats: List[Dict], parent_beat_num: int
    ) -> List[Dict]:
        """Remove placeholders associated with a specific parent beat."""
        return [beat for beat in beats if beat.get("parent_beat") != parent_beat_num]

    def _finalize_and_save_sequence(
        self, metadata: Dict, sequence_beats: List[Dict]
    ) -> None:
        """Finalize beat numbering, remove duplicates, and save the sequence."""
        sequence_beats = self._remove_duplicate_beats(sequence_beats)
        sequence_beats.sort(key=lambda beat: beat["beat"])
        self._update_beat_numbers(sequence_beats)
        self._save_sequence(metadata, sequence_beats)

    def _remove_duplicate_beats(self, beats: List[Dict]) -> List[Dict]:
        """Eliminate duplicate beats, keeping the first occurrence."""
        unique_beats = {}
        for beat in beats:
            beat_num = beat["beat"]
            if beat_num not in unique_beats:
                unique_beats[beat_num] = beat
        return list(unique_beats.values())

    def _update_beat_numbers(self, beats: List[Dict]) -> None:
        """Ensure beat numbers are consecutive and update parent beat references."""
        beat_mapping = {}
        for index, beat in enumerate(beats):
            old_beat_num = beat["beat"]
            beat_mapping[old_beat_num] = index
            beat["beat"] = index

        for beat in beats:
            if "parent_beat" in beat:
                beat["parent_beat"] = beat_mapping.get(
                    beat["parent_beat"], beat["parent_beat"]
                )

    def _save_sequence(self, metadata: Dict, beats: List[Dict]) -> None:
        """Save the updated sequence."""
        sequence_data = [metadata] + beats
        self.json_manager.loader_saver.save_current_sequence(sequence_data)
