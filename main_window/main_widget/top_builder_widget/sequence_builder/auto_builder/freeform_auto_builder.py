from copy import deepcopy
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from data.constants import BLUE, CLOCKWISE, COUNTER_CLOCKWISE, DASH, NO_ROT, RED, STATIC
from .turn_intensity_manager import TurnIntensityManager
import random

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.freeform_auto_builder_frame import (
        FreeformAutoBuilderFrame,
    )


class FreeFormAutoBuilder:
    def __init__(self, auto_builder_frame: "FreeformAutoBuilderFrame"):
        self.auto_builder_frame = auto_builder_frame
        self.sequence_widget = None
        self.top_builder_widget = (
            auto_builder_frame.auto_builder.sequence_builder.top_builder_widget
        )
        self.main_widget = self.top_builder_widget.main_widget
        self.sequence_builder = auto_builder_frame.auto_builder.sequence_builder
        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.validation_engine = self.main_widget.json_manager.validation_engine

    def build_sequence(
        self,
        beat_count: int,
        max_turn_intensity: int,
        level: int,
        max_turns: int,
        is_continuous_rot_dir,
    ):
        if not self.sequence_widget:
            self.sequence_widget = self.top_builder_widget.sequence_widget
        self.sequence = (
            self.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        self.modify_layout_for_chosen_number_of_beats(beat_count)
        turn_manager = TurnIntensityManager(
            max_turns, beat_count, level, max_turn_intensity
        )
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()
        if is_continuous_rot_dir:
            # Set an initial random rotation direction for both blue and red hands
            blue_rot_dir = random.choice(["cw", "ccw"])
            red_rot_dir = random.choice(["cw", "ccw"])
        else:
            blue_rot_dir = None
            red_rot_dir = None
        length_of_sequence_upon_start = len(self.sequence) - 2
        for i in range(beat_count - length_of_sequence_upon_start):
            next_pictograph = self._generate_next_pictograph(
                level,
                turns_blue[i],
                turns_red[i],
                is_continuous_rot_dir,
                blue_rot_dir,
                red_rot_dir,
            )

            self._update_dash_static_prop_rot_dirs(
                next_pictograph,
                is_continuous_rot_dir,
                blue_rot_dir,
                red_rot_dir,
            )
            self.sequence.append(next_pictograph)
            self.sequence_widget.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            self.validation_engine.validate_last_pictograph()
            QApplication.processEvents()
        self.top_builder_widget.sequence_builder.manual_builder.option_picker.update_option_picker(
            self.sequence
        )

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def _update_dash_static_prop_rot_dirs(
        self, next_pictograph_dict, is_continuous_rot_dir, red_rot_dir, blue_rot_dir
    ):
        """
        Update the prop rotation direction for dash or static motions.
        If continuous rotation is enabled, enforce the continuous rotation direction.
        """
        if next_pictograph_dict["blue_attributes"]["motion_type"] in [DASH, STATIC]:
            if is_continuous_rot_dir:
                next_pictograph_dict["blue_attributes"]["prop_rot_dir"] = (
                    blue_rot_dir
                    if next_pictograph_dict["blue_attributes"]["turns"] > 0
                    else NO_ROT
                )

        if next_pictograph_dict["red_attributes"]["motion_type"] in [DASH, STATIC]:
            if is_continuous_rot_dir:
                next_pictograph_dict["red_attributes"]["prop_rot_dir"] = (
                    red_rot_dir
                    if next_pictograph_dict["red_attributes"]["turns"] > 0
                    else NO_ROT
                )

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

    def _generate_next_pictograph(
        self,
        level: int,
        turn_blue: float,
        turn_red: float,
        is_continuous_rot_dir,
        blue_rot_dir,
        red_rot_dir,
    ):
        options = self.sequence_builder.manual_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )
        options = [deepcopy(option) for option in options]

        if is_continuous_rot_dir:
            options = self._filter_options_by_rotation(
                options, blue_rot_dir, red_rot_dir
            )

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

    def _filter_options_by_rotation(
        self, options: list[dict], blue_rot_dir, red_rot_dir
    ) -> list[dict]:
        """Filter options to match the rotation direction for both hands."""
        filtered_options = []
        for option in options:
            if option["blue_attributes"]["prop_rot_dir"] in [
                blue_rot_dir,
                NO_ROT,
            ] and option["red_attributes"]["prop_rot_dir"] in [red_rot_dir, NO_ROT]:
                filtered_options.append(option)

        # If no options match, fallback to the full list (could log a warning here)
        return filtered_options if filtered_options else options

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
