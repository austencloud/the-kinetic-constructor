from copy import deepcopy
import random
from typing import TYPE_CHECKING
from data.constants import BLUE, RED, DASH, STATIC, NO_ROT, CLOCKWISE, COUNTER_CLOCKWISE
from ....sequence_widget.beat_frame.start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from ....sequence_widget.sequence_widget import SequenceWidget
    from .base_auto_builder_frame import BaseAutoBuilderFrame


class AutoBuilderBase:
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        self.auto_builder_frame = auto_builder_frame
        self.sequence_widget: "SequenceWidget" = None
        self.top_builder_widget = (
            auto_builder_frame.auto_builder.sequence_builder.top_builder_widget
        )
        self.main_widget = self.top_builder_widget.main_widget
        self.sequence_builder = auto_builder_frame.auto_builder.sequence_builder
        self.validation_engine = self.main_widget.json_manager.validation_engine
        self.json_manager = self.main_widget.json_manager
        self.ori_calculator = self.main_widget.json_manager.ori_calculator

    def add_start_pos_pictograph(self):
        start_pos_keys = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        position_key = random.choice(start_pos_keys)
        self._add_start_position_to_sequence(position_key)

    def _add_start_position_to_sequence(self, position_key: str) -> None:
        start_pos, end_pos = position_key.split("_")
        letters = deepcopy(self.sequence_widget.main_widget.pictograph_dicts)
        for _, pictograph_dicts in letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict["start_pos"] == start_pos
                    and pictograph_dict["end_pos"] == end_pos
                ):
                    start_position_beat = StartPositionBeat(
                        self.top_builder_widget.sequence_widget.beat_frame
                    )
                    start_position_beat.updater.update_pictograph(
                        deepcopy(pictograph_dict)
                    )

                    self.main_widget.json_manager.start_position_handler.set_start_position_data(
                        start_position_beat
                    )
                    self.sequence_widget.beat_frame.start_pos_view.set_start_pos(
                        start_position_beat
                    )
                    return

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def _update_start_oris(self, next_pictograph_dict, last_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["start_ori"] = last_pictograph_dict[
            "blue_attributes"
        ]["end_ori"]
        next_pictograph_dict["red_attributes"]["start_ori"] = last_pictograph_dict[
            "red_attributes"
        ]["end_ori"]

    def _update_end_oris(self, next_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(next_pictograph_dict, BLUE)
        )
        next_pictograph_dict["red_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(next_pictograph_dict, RED)
        )

    def _update_dash_static_prop_rot_dirs(
        self, next_pictograph_dict, is_continuous_rot_dir, blue_rot_dir, red_rot_dir
    ):
        def update_prop_rot_dir(color, rot_dir):
            attributes = next_pictograph_dict[f"{color}_attributes"]
            if attributes["motion_type"] in [DASH, STATIC]:
                if is_continuous_rot_dir:
                    if attributes["turns"] > 0:
                        attributes["prop_rot_dir"] = rot_dir
                    else:
                        attributes["prop_rot_dir"] = NO_ROT
                else:
                    if attributes["turns"] > 0:
                        self._set_random_prop_rot_dir(next_pictograph_dict, color)
                    else:
                        attributes["prop_rot_dir"] = NO_ROT

        update_prop_rot_dir(BLUE, blue_rot_dir)
        update_prop_rot_dir(RED, red_rot_dir)

    def _set_random_prop_rot_dir(self, next_pictograph_dict, color):
        next_pictograph_dict[f"{color}_attributes"]["prop_rot_dir"] = random.choice(
            [CLOCKWISE, COUNTER_CLOCKWISE]
        )

    def _update_beat_number_depending_on_sequence_length(
        self, next_pictograph_dict, sequence
    ):
        next_pictograph_dict["beat"] = len(sequence) - 1
        return next_pictograph_dict

    def _filter_options_by_rotation(self, options: list[dict], blue_rot_dir, red_rot_dir) -> list[dict]:
        """Filter options to match the rotation direction for both hands."""
        filtered_options = [
            option for option in options
            if option["blue_attributes"]["prop_rot_dir"] in [blue_rot_dir, NO_ROT]
            and option["red_attributes"]["prop_rot_dir"] in [red_rot_dir, NO_ROT]
        ]
        return filtered_options if filtered_options else options
    
    def _set_turns(
        self, pictograph: dict, turn_blue: float, turn_red: float
    ) -> dict:
        pictograph["blue_attributes"]["turns"] = turn_blue
        pictograph["red_attributes"]["turns"] = turn_red
        return pictograph
