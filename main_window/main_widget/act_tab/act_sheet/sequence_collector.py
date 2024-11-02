# sequence_collector.py

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_sheet import ActSheet


class SequenceCollector:
    def __init__(self, act_sheet: "ActSheet"):
        self.act_sheet = act_sheet
        self.act_container = act_sheet.act_container

    def collect_sequences(self, total_rows=24):
        """Collect sequences, including cues, timestamps, and step labels for saving.
        Each sequence will track its length (e.g., 16 beats for 2 rows) and the rows it spans.
        """
        sequences = []
        row_index = 0

        while row_index < total_rows:
            # Determine the length of the current sequence (single or multi-row)
            sequence_length, sequence_rows = self._calculate_sequence_length_and_rows(
                row_index
            )
            sequence_data = {
                "sequence_start_marker": row_index == 0,
                "sequence_length": sequence_length,  # Total beat count (e.g., 16 for 2 rows of 8)
                "sequence_rows": sequence_rows,  # List of row indices this sequence spans
                "beats": [],
            }

            cue, timestamp = self.act_container.get_cue_timestamp_for_row(row_index)
            sequence_data["cue"] = cue
            sequence_data["timestamp"] = timestamp

            # Collect beats across all rows spanned by this sequence
            for row in sequence_rows:
                beat_views = self.act_container.get_beats_in_row(row)

                for beat_number in range(1, self.act_sheet.DEFAULT_COLUMNS + 1):
                    beat_view = (
                        beat_views[beat_number - 1]
                        if beat_number - 1 < len(beat_views)
                        else None
                    )
                    beat_data = {
                        "beat_number": beat_number
                        + row * self.act_sheet.DEFAULT_COLUMNS,
                        "pictograph_dict": (
                            beat_view.extract_metadata()
                            if beat_view and beat_view.is_populated()
                            else ""
                        ),
                        "step_label": (
                            self.act_container.beat_scroll.act_beat_frame.beat_step_map[
                                beat_view
                            ].label.text()
                            if beat_view
                            and beat_view
                            in self.act_container.beat_scroll.act_beat_frame.beat_step_map
                            else ""
                        ),
                    }
                    sequence_data["beats"].append(beat_data)

            sequences.append(sequence_data)
            row_index += len(
                sequence_rows
            )  # Move to the next set of rows after this sequence

        return sequences

    def _calculate_sequence_length_and_rows(self, start_row):
        """Calculate the sequence length and row span from the start_row."""
        # Assuming metadata to determine a sequence length or a default single row
        sequence_length = (
            8  # Placeholder for demo, e.g., could be determined dynamically
        )
        rows_needed = sequence_length // self.act_sheet.DEFAULT_COLUMNS
        sequence_rows = list(range(start_row, start_row + rows_needed))
        return sequence_length, sequence_rows
