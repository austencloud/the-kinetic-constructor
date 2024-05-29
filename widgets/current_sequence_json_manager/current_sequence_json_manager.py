from typing import TYPE_CHECKING, Union
from Enums.MotionAttributes import Color
from .json_sequence_loader_saver import JsonSequenceLoaderSaver
from .json_sequence_updater import JsonSequenceUpdater
from .json_start_position_handler import JsonStartPositionHandler
from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from .json_ori_calculator import JsonOriCalculator
from widgets.pictograph.pictograph import Pictograph
from widgets.current_sequence_json_manager.json_sequence_validation_engine import JsonSequenceValidationEngine

if TYPE_CHECKING:
    from widgets.json_manager import JSON_Manager


class CurrentSequenceJsonManager:
    def __init__(self, json_manager: "JSON_Manager") -> None:
        self.main_widget = json_manager.main_widget

        self.loader_saver = JsonSequenceLoaderSaver(self)
        self.updater = JsonSequenceUpdater(self)
        self.start_position_handler = JsonStartPositionHandler(self)
        self.ori_calculator = JsonOriCalculator(self)
        self.validation_engine = JsonSequenceValidationEngine(self)

    def clear_current_sequence_file(self):
        self.loader_saver.save_current_sequence([])

    def update_current_sequence_file_with_beat(self, beat_view: BeatView):
        sequence_data = self.loader_saver.load_current_sequence_json()
        if len(sequence_data) == 0:  # Make sure there's at least the metadata entry
            sequence_data.append(
                {
                    "prop_type": self.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                }
            )
        sequence_data.append(beat_view.beat.pictograph_dict)
        self.loader_saver.save_current_sequence(sequence_data)
        self.updater.update_sequence_properties()  # Recalculate circularity after each update
        self.main_widget.main_window.settings_manager.save_settings()  # Save state on change

    def clear_and_repopulate_the_current_sequence(self):
        self.clear_current_sequence_file()
        beat_frame = self.main_widget.top_builder_widget.sequence_widget.beat_frame
        beat_views = beat_frame.beats
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.start_position_handler.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view)
        self.main_widget.main_window.settings_manager.save_settings()  # Save state on change

    def get_index_for_pictograph(self, pictograph: Pictograph):
        sequence = self.loader_saver.load_current_sequence_json()
        for i, entry in enumerate(sequence):
            if entry == pictograph.pictograph_dict:
                return i
        return -1

    def update_turns_in_json_at_index(
        self, index: int, color: Color, turns: Union[int, float]
    ) -> None:
        self.updater.update_turns_in_json_at_index(index, color, turns)

    def update_start_pos_ori(self, color: Color, ori: int) -> None:
        self.start_position_handler.update_start_pos_ori(color, ori)

    def update_rot_dir_in_json_at_index(
        self, index: int, color: Color, prop_rot_dir: str
    ) -> None:
        self.updater.update_rot_dir_in_json_at_index(index, color, prop_rot_dir)

    def apply_turn_pattern_to_current_sequence(self, pattern: list[tuple]) -> None:
        self.updater.apply_turn_pattern_to_current_sequence(pattern)

    def get_red_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["red_attributes"]["end_ori"]
        return 0

    def get_blue_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["blue_attributes"]["end_ori"]
        return 0
