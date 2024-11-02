# act_populator.py

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .act_beat_frame import ActBeatFrame


class ActPopulator:
    def __init__(self, beat_frame: "ActBeatFrame"):
        self.beat_frame = beat_frame

    def create_initial_act_structure(self) -> dict:
        """Initialize the act structure with empty beats and metadata placeholders."""
        total_rows = (
            self.beat_frame.act_sheet.act_container.beat_scroll.act_beat_frame.layout_manager.calculate_total_rows()
        )

        act_data = {
            "title": self.beat_frame.act_sheet.act_header.get_title(),
            "prop_type": self.beat_frame.main_widget.prop_type.name,
            "grid_mode": self.beat_frame.main_widget.settings_manager.global_settings.get_grid_mode(),
            "sequences": [],
        }

        for row in range(total_rows):
            row_data = {
                "sequence_start_marker": row == 0,
                "cue": "",
                "timestamp": "",
                "beats": [
                    {"step_label": "", "is_filled": False} for _ in range(8)
                ],  # 8 beats per row
            }
            act_data["sequences"].append(row_data)
        return act_data

    def populate_beats(self, sequence_data: dict):
        """Populate act beats and save the updated act structure."""
        beats = sequence_data.get("sequence", [])
        start_index = self.find_next_available_beat_index()

        for i, beat_data in enumerate(beats):
            if i < 2:
                continue
            current_index = start_index + i
            if current_index % 8 == 0:
                cue = beat_data.get("cue", "")
                timestamp = beat_data.get("timestamp", "")
                self.add_cue_and_timestamp(current_index, cue, timestamp)

            self.populate_beat(current_index - 2, beat_data)

        # Save the updated act
        self.save_populated_act()


    def find_next_available_beat_index(self) -> int:
        """Find the next empty beat index in the act to start the new sequence."""
        for index, beat_view in enumerate(self.beat_frame.beats):
            if not beat_view.is_populated():
                return index
        return len(self.beat_frame.beats)

    def add_cue_and_timestamp(self, beat_index: int, cue: str, timestamp: str):
        """Attach cue and timestamp to the corresponding row."""
        row_index = beat_index // 8
        cue_label = f"{timestamp} - {cue}"

    def populate_beat(self, beat_index: int, beat_data: dict):
        """Populate an individual beat with its metadata."""
        if beat_index < len(self.beat_frame.beats):
            beat_view = self.beat_frame.beats[beat_index]
            step_label_text = beat_data.get("step_label", "")
            beat_view.beat.updater.update_pictograph(beat_data)
            beat_view.beat.pictograph_dict = beat_data
            self.add_step_label(beat_view, step_label_text)

    def add_step_label(self, beat_view, label_text: str):
        """Attach step label to an individual beat view."""
        if beat_view in self.beat_frame.beat_step_map:
            step_label = self.beat_frame.beat_step_map[beat_view]
            step_label.label.setText(label_text)

    def save_initial_act_structure(self):
        """Create and save an initial act structure with empty beats."""
        act_data = self.create_initial_act_structure()
        self.beat_frame.main_widget.json_manager.save_act(act_data)

    def save_populated_act(self):
        """Save the populated act structure."""
        act_data = self.create_initial_act_structure()  # Start with the frame
        act_data["sequences"] = self.collect_sequences()
        self.beat_frame.main_widget.json_manager.save_act(act_data)
        
    def collect_sequences(self):
        """Collect sequences including cues, timestamps, and step labels for saving."""
        sequences = []
        total_rows = (
            self.beat_frame.act_sheet.act_container.beat_scroll.act_beat_frame.layout_manager.calculate_total_rows()
        )

        for row in range(total_rows):
            # Get cue and timestamp for each row
            cue, timestamp = (
                self.beat_frame.act_sheet.act_container.get_cue_timestamp_for_row(row)
            )
            sequence_data = {
                "sequence_start_marker": row == 0,
                "cue": cue,
                "timestamp": timestamp,
                "beats": [],
            }

            # Retrieve each beat view in the current row
            beat_views = self.beat_frame.act_sheet.act_container.get_beats_in_row(row)
            for beat_view in beat_views:
                if not beat_view.is_populated():
                    continue
                beat_data = beat_view.extract_metadata()
                beat_data["step_label"] = self.beat_frame.beat_step_map[
                    beat_view
                ].label.text()
                sequence_data["beats"].append(beat_data)

            if sequence_data["beats"]:
                sequences.append(sequence_data)

        return sequences
