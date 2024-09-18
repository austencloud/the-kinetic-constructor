from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
import random
from copy import deepcopy
from PyQt6.QtCore import Qt
from data.constants import BLUE, RED, NO_ROT, CLOCKWISE, COUNTER_CLOCKWISE
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_classes.base_auto_builder import AutoBuilderBase
from ..turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from .freeform_auto_builder_frame import FreeformAutoBuilderFrame

class FreeFormAutoBuilder(AutoBuilderBase):
    def __init__(self, auto_builder_frame: "FreeformAutoBuilderFrame"):
        super().__init__(auto_builder_frame)
        # Any additional initialization for FreeFormAutoBuilder can go here

    def build_sequence(
        self,
        beat_count: int,
        max_turn_intensity: int,
        level: int,
        is_continuous_rot_dir: bool,
    ):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if not self.sequence_widget:
            self.sequence_widget = self.top_builder_widget.sequence_widget
        self.sequence = self.json_manager.loader_saver.load_current_sequence_json()
        self.modify_layout_for_chosen_number_of_beats(beat_count)

        if len(self.sequence) == 1:
            self.add_start_pos_pictograph()
            self.sequence = self.json_manager.loader_saver.load_current_sequence_json()

        turn_manager = TurnIntensityManager(beat_count, level, max_turn_intensity)
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()
        if is_continuous_rot_dir:
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
            self.sequence.append(next_pictograph)
            self.sequence_widget.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            self.validation_engine.validate_last_pictograph()
            QApplication.processEvents()

        self.sequence_widget.top_builder_widget.sequence_builder.manual_builder.transition_to_sequence_building()
        self.top_builder_widget.sequence_builder.manual_builder.option_picker.update_option_picker(self.sequence)
        QApplication.restoreOverrideCursor()

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
            options = self._filter_options_by_rotation(options, blue_rot_dir, red_rot_dir)

        last_beat = self.sequence[-1]
        chosen_option = random.choice(options)

        self._update_start_oris(chosen_option, last_beat)
        self._update_end_oris(chosen_option)

        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2 or level == 3:
            chosen_option = self._apply_level_2_or_3_constraints(chosen_option, turn_blue, turn_red)

        self._update_dash_static_prop_rot_dirs(
            chosen_option,
            is_continuous_rot_dir,
            blue_rot_dir,
            red_rot_dir,
        )
        chosen_option = self._update_beat_number_depending_on_sequence_length(
            chosen_option, self.sequence
        )
        return chosen_option

    def _filter_options_by_rotation(self, options: list[dict], blue_rot_dir, red_rot_dir) -> list[dict]:
        """Filter options to match the rotation direction for both hands."""
        filtered_options = []
        for option in options:
            if option["blue_attributes"]["prop_rot_dir"] in [blue_rot_dir, NO_ROT] and \
               option["red_attributes"]["prop_rot_dir"] in [red_rot_dir, NO_ROT]:
                filtered_options.append(option)
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
