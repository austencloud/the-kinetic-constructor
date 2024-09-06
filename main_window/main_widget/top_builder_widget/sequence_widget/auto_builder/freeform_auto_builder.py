from copy import deepcopy
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from data.constants import BLUE, CLOCKWISE, COUNTER_CLOCKWISE, DASH, RED, STATIC
from .turn_intensity_manager import TurnIntensityManager
import random

if TYPE_CHECKING:
    from .freeform_auto_builder_dialog import FreeformAutoBuilderDialog


class FreeFormAutoBuilder:
    def __init__(self, auto_builder_dialog: "FreeformAutoBuilderDialog"):
        self.auto_builder_dialog = auto_builder_dialog
        self.sequence_widget = auto_builder_dialog.sequence_widget

        self.ori_calculator = (
            self.sequence_widget.main_widget.json_manager.ori_calculator
        )
        self.validation_engine = (
            self.sequence_widget.main_widget.json_manager.validation_engine
        )

    def build_sequence(
        self, beat_count: int, max_turn_intensity: int, level: int, max_turns: int
    ):
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        self.modify_layout_for_chosen_number_of_beats(beat_count)
        turn_manager = TurnIntensityManager(
            max_turns, beat_count, level, max_turn_intensity
        )
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()

        length_of_sequence_upon_start = len(self.sequence) - 2
        for i in range(beat_count - length_of_sequence_upon_start):
            next_pictograph = self._generate_next_pictograph(
                level,
                turns_blue[i],
                turns_red[i],
            )

            self._update_dash_static_prop_rot_dirs(next_pictograph)

            self.sequence.append(next_pictograph)
            self.sequence_widget.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            self.validation_engine.validate_last_pictograph()
            QApplication.processEvents()
        self.sequence_widget.top_builder_widget.sequence_builder.option_picker.update_option_picker(
            self.sequence
        )

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.auto_builder_dialog.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def _update_dash_static_prop_rot_dirs(self, next_pictograph_dict):
        if (
            next_pictograph_dict["blue_attributes"]["motion_type"] in [DASH, STATIC]
            and next_pictograph_dict["blue_attributes"]["turns"] > 0
        ):
            self._set_default_prop_rot_dir(next_pictograph_dict, BLUE)
        if (
            next_pictograph_dict["red_attributes"]["motion_type"] in [DASH, STATIC]
            and next_pictograph_dict["red_attributes"]["turns"] > 0
        ):
            self._set_default_prop_rot_dir(next_pictograph_dict, RED)

    def _set_default_prop_rot_dir(self, next_pictograph_dict, color):
        # Set the prop rot dir randomly between CLOCKWISE and COUNTERCLOCKWISE
        next_pictograph_dict[color + "_attributes"]["prop_rot_dir"] = random.choice(
            [CLOCKWISE, COUNTER_CLOCKWISE]
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

    def _generate_next_pictograph(self, level: int, turn_blue: float, turn_red: float):
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )
        options = [deepcopy(option) for option in options]

        last_beat = self.sequence[-1]
        chosen_option = random.choice(options)

        self._update_start_oris(chosen_option, last_beat)
        self._update_end_oris(chosen_option)

        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2:
            chosen_option = self._apply_level_2_or_3_constraints(
                chosen_option, turn_blue, turn_red
            )
        elif level == 3:
            chosen_option = self._apply_level_2_or_3_constraints(
                chosen_option, turn_blue, turn_red
            )
        return chosen_option

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_or_3_constraints(
        self, pictograph: dict, turn_blue: float, turn_red: float
    ) -> dict:
        pictograph["blue_attributes"]["turns"] = turn_blue
        pictograph["red_attributes"]["turns"] = turn_red
        return pictograph
