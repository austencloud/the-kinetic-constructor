import random
from typing import TYPE_CHECKING
from data.constants import BLUE, RED, DASH, STATIC
from data.position_maps import (
    half_position_map,
    quarter_position_map_cw,
    quarter_position_map_ccw,
)
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from .turn_intensity_manager import TurnIntensityManager
from ..sequence_auto_completer.rotational_permutation_executor import (
    RotationalPermutationExecuter,
)

if TYPE_CHECKING:
    from .circular_auto_builder_dialog import CircularAutoBuilderDialog


class CircularAutoBuilder:
    def __init__(self, auto_builder_dialog: "CircularAutoBuilderDialog"):
        self.auto_builder_dialog = auto_builder_dialog
        self.sequence_widget = auto_builder_dialog.sequence_widget
        self.validation_engine = (
            self.sequence_widget.main_widget.json_manager.validation_engine
        )

    def build_sequence(
        self,
        length: int,
        turn_intensity: int,
        level: int,
        max_turns: int,
        rotation_type: str,
    ):
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )

        word_length = length // 4  # Assuming 4 beats per repetition
        turn_manager = TurnIntensityManager(max_turns, word_length, level)
        turns = turn_manager.allocate_turns()

        self.modify_layout_for_chosen_number_of_beats(length)

        # Generate the initial segment of the sequence
        sequence = self.sequence
        length_without_sequence_properties_or_start_pos = len(sequence) - 2
        available_range = word_length - length_without_sequence_properties_or_start_pos
        for i in range(available_range):
            is_last_in_quarter = (
                i == word_length - length_without_sequence_properties_or_start_pos - 1
            )

            last_pictograph = sequence[-1]
            next_pictograph = self._generate_next_pictograph(
                level, turns[i], is_last_in_quarter, rotation_type
            )
            self._update_start_oris(next_pictograph, last_pictograph)
            self._update_end_oris(next_pictograph)
            self._update_dash_static_prop_rot_dirs(next_pictograph)
            next_pictograph = self._update_beat_number_depending_on_sequence_length(
                next_pictograph, sequence
            )
            sequence.append(next_pictograph)
            self.sequence_widget.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            self.validation_engine.validate_last_pictograph()

        self.sequence_widget.json_manager.updater.update_sequence_properties()
        self.sequence_widget.json_manager.loader_saver.save_current_sequence(sequence)
        self._apply_strict_rotational_permutations(sequence)

        self._finalize_sequence(sequence, length)

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.auto_builder_dialog.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def _generate_next_pictograph(
        self, level: int, turn: float, is_last_in_quarter: bool, rotation_type: str
    ) -> dict:
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )

        if is_last_in_quarter:
            expected_end_pos = self._determine_expected_end_pos(rotation_type)
            chosen_option = self._select_pictograph_with_end_pos(
                options, expected_end_pos
            )
        else:
            chosen_option = random.choice(options)

        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2:
            chosen_option = self._apply_level_2_constraints(chosen_option, turn)
        elif level == 3:
            chosen_option = self._apply_level_3_constraints(chosen_option, turn)

        return chosen_option

    def _apply_level_1_constraints(self, pictograph: dict) -> dict:
        pictograph["blue_attributes"]["turns"] = 0
        pictograph["red_attributes"]["turns"] = 0
        return pictograph

    def _apply_level_2_constraints(self, pictograph: dict, turn: float) -> dict:
        pictograph["blue_attributes"]["turns"] = turn
        pictograph["red_attributes"]["turns"] = turn
        return pictograph

    def _apply_level_3_constraints(self, pictograph: dict, turn: float) -> dict:
        pictograph["blue_attributes"]["turns"] = turn
        pictograph["red_attributes"]["turns"] = turn
        return pictograph

    def _determine_expected_end_pos(self, rotation_type: str) -> str:
        """Determine the expected end position based on rotation type and current sequence."""
        start_pos = self.sequence[1]["end_pos"]

        if rotation_type == "quartered":
            # Randomly choose between CW and CCW for more flexibility
            if random.choice([True, False]):
                return quarter_position_map_cw[start_pos]
            else:
                return quarter_position_map_ccw[start_pos]
        elif rotation_type == "halved":
            return half_position_map[start_pos]
        else:
            print("Invalid rotation type - expected 'quartered' or 'halved'")
            return None  # Default case, should not happen

    def _select_pictograph_with_end_pos(
        self, options: list[dict], expected_end_pos: str
    ) -> dict:
        """Select a pictograph from options that has the desired end position."""
        valid_options = [
            option for option in options if option["end_pos"] == expected_end_pos
        ]
        if not valid_options:
            raise ValueError(
                f"No valid pictograph found with end position {expected_end_pos}."
            )
        return random.choice(valid_options)

    def _update_start_oris(self, next_pictograph_dict, last_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["start_ori"] = last_pictograph_dict[
            "blue_attributes"
        ]["end_ori"]
        next_pictograph_dict["red_attributes"]["start_ori"] = last_pictograph_dict[
            "red_attributes"
        ]["end_ori"]

    def _update_end_oris(self, next_pictograph_dict):
        next_pictograph_dict["blue_attributes"]["end_ori"] = (
            self.sequence_widget.main_widget.json_manager.ori_calculator.calculate_end_orientation(
                next_pictograph_dict, BLUE
            )
        )
        next_pictograph_dict["red_attributes"]["end_ori"] = (
            self.sequence_widget.main_widget.json_manager.ori_calculator.calculate_end_orientation(
                next_pictograph_dict, RED
            )
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
        next_pictograph_dict[color + "_attributes"]["prop_rot_dir"] = random.choice(
            ["cw", "ccw"]
        )

    def _apply_strict_rotational_permutations(self, sequence: list[dict]) -> None:
        executor = RotationalPermutationExecuter(self.auto_builder_dialog)
        executor.create_permutations(sequence)

    def _finalize_sequence(self, sequence: list[dict], length: int) -> None:
        self.sequence_widget.main_widget.json_manager.loader_saver.save_current_sequence(
            sequence
        )
        self.sequence_widget.beat_frame.populate_beat_frame_from_json(sequence)
        # self.sequence_widget.autocompleter.auto_complete_sequence()

    def _update_beat_number_depending_on_sequence_length(
        self, next_pictograph_dict, sequence
    ):
        dict_with_beat_number = {}
        dict_with_beat_number["beat"] = len(sequence) - 1
        for key in next_pictograph_dict:
            if key != "beat":
                dict_with_beat_number[key] = next_pictograph_dict[key]
        next_pictograph_dict = dict_with_beat_number
        return next_pictograph_dict
