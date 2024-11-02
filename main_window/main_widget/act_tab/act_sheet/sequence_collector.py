# sequence_collector.py
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_sheet.act_sheet import ActSheet


class SequenceCollector:
    def __init__(self, act_sheet: "ActSheet"):
        self.act_sheet = act_sheet
        self.act_container = act_sheet.act_container

    def collect_sequences(self, total_rows=24):
        """Collect sequences, including cues, timestamps, and step labels for saving."""
        sequences = []

        for i in range(total_rows):
            sequence_data = {
                "sequence_start_marker": True,
                "beats": [],
            }
            cue, timestamp = self.act_container.get_cue_timestamp_for_row(i)
            sequence_data["cue"] = cue
            sequence_data["timestamp"] = timestamp

            # Collect beats for the row, ensuring each beat position is represented
            beat_views = self.act_container.get_beats_in_row(i)

            for beat_number in range(1, self.act_sheet.DEFAULT_COLUMNS + 1):
                if beat_number - 1 < len(beat_views):
                    beat_view = beat_views[beat_number - 1]
                    beat_data = {
                        "beat_number": beat_number,
                        "pictograph_dict": (
                            beat_view.extract_metadata()
                            if beat_view.is_populated()
                            else ""
                        ),
                        "step_label": (
                            self.act_container.beat_scroll.act_beat_frame.beat_step_map[beat_view].label.text()
                            if beat_view in self.act_container.beat_scroll.act_beat_frame.beat_step_map
                            else ""
                        ),
                    }
                else:
                    # Placeholder for missing beats
                    beat_data = {
                        "beat_number": beat_number,
                        "pictograph_dict": "",
                        "step_label": "",
                    }

                sequence_data["beats"].append(beat_data)

            sequences.append(sequence_data)

        return sequences
