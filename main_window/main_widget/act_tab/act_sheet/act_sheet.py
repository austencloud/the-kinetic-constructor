from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from .act_header.act_header import ActHeader
from .act_splitter.act_container import ActContainer
import os
import json
from PyQt6.QtCore import QDir

if TYPE_CHECKING:
    from ..act_tab import ActTab


class ActSheet(QWidget):
    DEFAULT_ROWS = 24
    DEFAULT_COLUMNS = 8

    def __init__(self, act_tab: "ActTab") -> None:
        super().__init__(act_tab)
        self.act_tab = act_tab
        self.main_widget = act_tab.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager.act_sheet
        self.act_header = ActHeader(self)
        self.act_container = ActContainer(self)
        self.setAcceptDrops(False)

        self._setup_layout()
        self.act_container.connect_scroll_sync()

    def save_act_to_json(self, filename="current_act.json"):
        """Save the current act to a JSON file in the acts directory."""
        act_data = {
            "title": self.act_header.get_title(),
            "prop_type": self.main_widget.prop_type.name,
            "grid_mode": self.main_widget.settings_manager.global_settings.get_grid_mode(),
            "sequences": self._collect_sequences(),
        }
        acts_dir = os.path.join(QDir.currentPath(), "acts")
        os.makedirs(acts_dir, exist_ok=True)
        file_path = os.path.join(acts_dir, filename)

        with open(file_path, "w") as f:
            json.dump(act_data, f, indent=4)
        print(f"Act saved to {file_path}")

    def load_act_from_json(self, filename="current_act.json"):
        """Load an act from a JSON file in the acts directory."""
        file_path = os.path.join(QDir.currentPath(), "acts", filename)
        if not os.path.isfile(file_path):
            print(f"No saved act found at {file_path}")
            return

        with open(file_path, "r") as f:
            act_data = json.load(f)
        self.populate_from_act_data(act_data)

    def _collect_sequences(self):
        """Collect sequences including cues, timestamps, and step labels for saving."""
        sequences = []
        total_rows = (
            self.act_container.beat_scroll.act_beat_frame.layout_manager.calculate_total_rows()
        )

        for i in range(total_rows):
            sequence_data = {
                "sequence_start_marker": i == 0,
                "beats": [],
            }
            cue, timestamp = self.act_container.get_cue_timestamp_for_row(i)
            sequence_data["cue"] = cue
            sequence_data["timestamp"] = timestamp

            # Retrieve the beat views for the row and ensure we have the expected number of columns
            beat_views = self.act_container.get_beats_in_row(i)

            for beat_number in range(1, self.DEFAULT_COLUMNS + 1):
                if beat_number - 1 < len(beat_views):
                    # Use the existing beat view if available
                    beat_view = beat_views[beat_number - 1]
                    beat_data = {
                        "beat_number": beat_number,
                        "pictograph_dict": (
                            beat_view.extract_metadata()
                            if beat_view.is_populated()
                            else ""
                        ),
                        "step_label": (
                            self.act_container.beat_scroll.act_beat_frame.beat_step_map[
                                beat_view
                            ].label.text()
                            if beat_view
                            in self.act_container.beat_scroll.act_beat_frame.beat_step_map
                            else ""
                        ),
                    }
                else:
                    # Create a placeholder for missing beats
                    beat_data = {
                        "beat_number": beat_number,
                        "pictograph_dict": "",
                        "step_label": "",
                    }

                sequence_data["beats"].append(beat_data)

            sequences.append(sequence_data)

        return sequences

    def populate_from_act_data(self, act_data: dict):
        """Populate ActSheet from saved JSON data."""
        self.act_header.set_title(act_data.get("title", "Untitled Act"))
        self.main_widget.manager.set_grid_mode(act_data.get("grid_mode", "diamond"))

        for sequence in act_data["sequences"]:
            self.act_container.beat_scroll.act_beat_frame.populator.populate_beats(
                sequence
            )

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.act_header, 1)
        layout.addWidget(self.act_container, 10)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resize_act_sheet(self):
        """Resize each part when ActSheet resizes."""
        self.act_header.resize_header_widget()
        self.act_container.beat_scroll.act_beat_frame.resize_act_beat_frame()
        self.act_container.cue_scroll.resize_cue_scroll()

    def closeEvent(self, event):
        self.act_container.save_scrollbar_state()
        super().closeEvent(event)

    def showEvent(self, event):
        self.act_container.restore_scrollbar_state()
        super().showEvent(event)
