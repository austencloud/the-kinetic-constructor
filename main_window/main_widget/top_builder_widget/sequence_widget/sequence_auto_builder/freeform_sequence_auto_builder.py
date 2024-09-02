from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication

from data.constants import BLUE, CLOCKWISE, COUNTER_CLOCKWISE, DASH, RED, STATIC
from .turn_intensity_manager import TurnIntensityManager
import random

if TYPE_CHECKING:
    from .sequence_auto_builder import SequenceAutoBuilder

class FreeFormSequenceAutoBuilder:
    def __init__(self, auto_builder_dialog: "SequenceAutoBuilder"):
        self.auto_builder_dialog = auto_builder_dialog
        self.sequence_widget = auto_builder_dialog.sequence_widget

        self.ori_calculator = (
            self.sequence_widget.main_widget.json_manager.ori_calculator
        )
        self.validation_engine = (
            self.sequence_widget.main_widget.json_manager.validation_engine
        )

    def build_sequence(self, length: int, turn_intensity: int, level: int, max_turns: int):
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        turn_manager = TurnIntensityManager(max_turns, length, level)
        turns = turn_manager.allocate_turns()

        length_of_sequence_upon_start = len(self.sequence) - 2
        for i in range(length - length_of_sequence_upon_start):
            next_pictograph_dict = self._generate_next_pictograph(level, turns[i])

            self._update_end_oris(next_pictograph_dict)
            self._update_dash_static_prop_rot_dirs(next_pictograph_dict)

            self.sequence.append(next_pictograph_dict)
            self.sequence_widget.create_new_beat_and_add_to_sequence(next_pictograph_dict)
            self.validation_engine.validate_last_pictograph()
            self.sequence_widget.top_builder_widget.sequence_builder.option_picker.update_option_picker(
                self.sequence
            )
            QApplication.processEvents()

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

    def _update_end_oris(self, next_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(next_pictograph_dict, BLUE)
        )
        next_pictograph_dict["red_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(next_pictograph_dict, RED)
        )

    def _generate_next_pictograph(self, level: int, turn: float) -> dict:
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )
        chosen_option = random.choice(options)

        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2:
            chosen_option = self._apply_level_2_constraints(chosen_option, turn)
        elif level == 3:
            chosen_option = self._apply_level_3_constraints(chosen_option, turn)

        return chosen_option

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        # No turns, only radial orientations
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_constraints(self, pictograph: dict, turn: float) -> dict:
        # Apply the pre-determined turn
        pictograph["blue_attributes"]["turns"] = turn
        pictograph["red_attributes"]["turns"] = turn
        return pictograph

    def _apply_level_3_constraints(self, pictograph: dict, turn: float) -> dict:
        # Apply the pre-determined turn with potential non-radial orientations
        pictograph["blue_attributes"]["turns"] = turn
        pictograph["red_attributes"]["turns"] = turn
        return pictograph
