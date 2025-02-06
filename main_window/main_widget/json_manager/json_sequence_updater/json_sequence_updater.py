from typing import TYPE_CHECKING
from main_window.main_widget.sequence_widget.beat_frame.beat import Beat
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from .json_duration_updater import JsonDurationUpdater
from .json_prop_rot_dir_updater import JsonstrUpdater
from .json_prop_type_updater import JsonPropTypeUpdater
from .json_letter_updater import JsonLetterUpdater
from .json_motion_type_updater import JsonMotionTypeUpdater
from .json_turns_updater import JsonTurnsUpdater


if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_manager import JsonManager


class JsonSequenceUpdater:
    def __init__(self, json_manager: "JsonManager"):
        self.json_manager = json_manager
        self.main_widget = json_manager.main_widget
        self.turns_updater = JsonTurnsUpdater(self)
        self.motion_type_updater = JsonMotionTypeUpdater(self)
        self.prop_type_updater = JsonPropTypeUpdater(self)
        self.letter_updater = JsonLetterUpdater(self)
        self.prop_rot_dir_updater = JsonstrUpdater(self)
        self.duration_updater = JsonDurationUpdater(self)

    def update_current_sequence_file_with_beat(self, beat: Beat):
        view = beat.view
        sequence_data = self.json_manager.loader_saver.load_current_sequence_json()
        sequence_metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        sequence_beats = sequence_data[1:]

        beat_data = beat.pictograph_dict.copy()
        beat_data["duration"] = beat.duration
        number = self.get_next_beat_number(sequence_beats)
        view.number = number
        beat_data["beat"] = number

        sequence_beats.append(beat_data)

        for beat_num in range(view.number + 1, view.number + beat.duration):
            placeholder_entry = {
                "beat": beat_num,
                "is_placeholder": True,
                "parent_beat": view.number,
            }
            sequence_beats.append(placeholder_entry)

        sequence_beats.sort(key=lambda entry: entry.get("beat", float("inf")))
        sequence_data = [sequence_metadata] + sequence_beats

        self.json_manager.loader_saver.save_current_sequence(sequence_data)

    def get_next_beat_number(self, sequence_beats):
        if not sequence_beats:
            return 1
        return max(beat["beat"] for beat in sequence_beats) + 1

    def add_placeholder_entry_to_current_sequence(
        self, beat_num: int, parent_beat: int
    ):
        sequence_data = self.json_manager.loader_saver.load_current_sequence_json()
        sequence_metadata = sequence_data[0] if "word" in sequence_data[0] else {}
        sequence_beats = sequence_data[1:]

        placeholder_entry = {
            "beat": beat_num,
            "is_placeholder": True,
            "parent_beat": parent_beat,
        }
        sequence_beats.append(placeholder_entry)

        sequence_beats.sort(key=lambda entry: entry.get("beat", float("inf")))
        sequence_data = [sequence_metadata] + sequence_beats

        self.json_manager.loader_saver.save_current_sequence(sequence_data)

    def clear_and_repopulate_json_from_beat_view(self):
        self.json_manager.loader_saver.clear_current_sequence_file()
        beat_frame = self.json_manager.main_widget.sequence_widget.beat_frame
        beat_views = beat_frame.beat_views
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.json_manager.start_pos_handler.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view.beat)
