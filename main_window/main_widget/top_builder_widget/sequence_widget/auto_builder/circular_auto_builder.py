from copy import deepcopy
import random
from typing import TYPE_CHECKING
from data.constants import BLUE, NO_ROT, RED, DASH, STATIC
from data.position_maps import (
    half_position_map,
    quarter_position_map_cw,
    quarter_position_map_ccw,
)
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from main_window.main_widget.top_builder_widget.sequence_widget.sequence_auto_completer.mirrored_permutation_executor import (
    MirroredPermutationExecutor,
)
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
        self.json_manager = self.sequence_widget.main_widget.json_manager
        self.beat_frame = self.sequence_widget.beat_frame
        self.rotational_executor = RotationalPermutationExecuter(self)
        self.mirrored_executor = MirroredPermutationExecutor(self, False)
        self.rotation_direction = None  # Track the continuous rotation direction

    def build_sequence(
        self,
        length: int,
        max_turn_intensity: int,
        level: int,
        max_turns: int,
        rotation_type: str,
        permutation_type: str,
        is_continuous_rot_dir: str,
    ):
        # Building the base sequence
        self.sequence = (
            self.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
        )
        length_without_sequence_properties_or_start_pos = len(self.sequence) - 2
        if permutation_type == "rotational":
            if rotation_type == "quartered":
                word_length = length // 4
            elif rotation_type == "halved":
                word_length = length // 2
            available_range = (
                word_length - length_without_sequence_properties_or_start_pos
            )
        elif permutation_type == "mirrored":
            word_length = length // 2
            available_range = (
                word_length - length_without_sequence_properties_or_start_pos
            )

        turn_manager = TurnIntensityManager(
            max_turns, word_length, level, max_turn_intensity
        )

        # Allocate turns for both blue and red motions
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()

        if is_continuous_rot_dir:
            # Set an initial random rotation direction for both blue and red hands
            blue_rot_dir = random.choice(["cw", "ccw"])
            red_rot_dir = random.choice(["cw", "ccw"])
        else:
            blue_rot_dir = None
            red_rot_dir = None
        self.modify_layout_for_chosen_number_of_beats(length)

        if len(self.sequence) == 1:
            self.add_start_pos_pictograph()
            length_without_sequence_properties_or_start_pos = len(self.sequence) - 2

        # Generate the initial segment of the sequence
        for i in range(available_range):
            is_last_in_word = (
                i == word_length - length_without_sequence_properties_or_start_pos - 1
            )

            last_pictograph = self.sequence[-1]
            next_pictograph = self._generate_next_pictograph(
                level,
                turns_blue[i],
                turns_red[i],
                is_last_in_word,
                rotation_type,
                permutation_type,
                is_continuous_rot_dir,
                blue_rot_dir,
                red_rot_dir,
            )
            self._update_start_oris(next_pictograph, last_pictograph)
            self._update_end_oris(next_pictograph)
            self._update_dash_static_prop_rot_dirs(
                next_pictograph,
                is_continuous_rot_dir,
                blue_rot_dir,
                red_rot_dir,
            )
            next_pictograph = self._update_beat_number_depending_on_sequence_length(
                next_pictograph, self.sequence
            )
            self.sequence.append(next_pictograph)
            self.sequence_widget.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            self.validation_engine.validate_last_pictograph()

        self._apply_permutations(self.sequence, permutation_type, rotation_type)

    def add_start_pos_pictograph(self):
        # get one of the start positions from the default
        start_pos = ["alpha1_alpha1", "beta3_beta3", "gamma6_gamma6"]
        for i, position_key in enumerate(start_pos):
            self._add_start_position_to_sequence(position_key)

    def _add_start_position_to_sequence(self, position_key: str) -> None:
        # get it from the main widget letters, amke a copy, and put it into the sequence
        start_pos, end_pos = position_key.split("_")
        for (
            letter,
            pictograph_dicts,
        ) in self.sequence_widget.main_widget.letters.items():
            for pictograph_dict in pictograph_dicts:
                if (
                    pictograph_dict["start_pos"] == start_pos
                    and pictograph_dict["end_pos"] == end_pos
                ):
                    pictograph_dict = deepcopy(pictograph_dict)
                    self.sequence.append(pictograph_dict)
                    return

    def _apply_permutations(
        self, sequence: list[dict], permutation_type: str, rotation_type: str
    ) -> None:
        if permutation_type == "rotational":
            if self.can_perform_rotational_permutation(sequence, rotation_type):
                self.rotational_executor.create_permutations(sequence)
        elif permutation_type == "mirrored":
            if self.mirrored_executor.can_perform_mirrored_permutation(sequence):
                self.mirrored_executor.create_permutations(sequence, "vertical")

    def can_perform_rotational_permutation(
        self, sequence: list[dict], rotation_type: str
    ) -> bool:
        # Check if the sequence satisfies conditions for rotational or mirrored permutations
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        if rotation_type == "quartered":
            return (start_pos, end_pos) in quartered_permutations
        elif rotation_type == "halved":
            return (start_pos, end_pos) in halved_permutations

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.auto_builder_dialog.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )

    def _generate_next_pictograph(
        self,
        level: int,
        turn_blue: float,
        turn_red: float,
        is_last_in_word: bool,
        rotation_type: str,
        permutation_type: str,
        is_continuous_rot_dir,
        blue_rot_dir,
        red_rot_dir,
    ) -> dict:
        # Get the next set of options (these come from the letters dictionary)
        options = self.sequence_widget.top_builder_widget.sequence_builder.option_picker.option_getter.get_next_options(
            self.sequence
        )

        # Ensure that we are working on a deep copy of the options to avoid modifying the original data
        options = [deepcopy(option) for option in options]

        # Filter the options to match the rotation direction if continuous rotation is enabled
        if is_continuous_rot_dir:
            options = self._filter_options_by_rotation(
                options, blue_rot_dir, red_rot_dir
            )

        if permutation_type == "rotational":
            if is_last_in_word:
                expected_end_pos = self._determine_rotational_end_pos(rotation_type)
                chosen_option = self._select_pictograph_with_end_pos(
                    options, expected_end_pos
                )
            else:
                chosen_option = random.choice(options)

        elif permutation_type == "mirrored":
            if is_last_in_word:
                expected_end_pos = self.sequence[1]["end_pos"]
                chosen_option = self._select_pictograph_with_end_pos(
                    options, expected_end_pos
                )
            else:
                chosen_option = random.choice(options)

        # Apply the necessary level-specific constraints
        if level == 1:
            chosen_option = self._apply_level_1_constraints(chosen_option)
        elif level == 2 or level == 3:
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

    def _determine_rotational_end_pos(self, rotation_type: str) -> str:
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
            else:
                self._set_default_prop_rot_dir(next_pictograph_dict, BLUE)

        if next_pictograph_dict["red_attributes"]["motion_type"] in [DASH, STATIC]:
            if is_continuous_rot_dir:
                next_pictograph_dict["red_attributes"]["prop_rot_dir"] = (
                    red_rot_dir
                    if next_pictograph_dict["red_attributes"]["turns"] > 0
                    else NO_ROT
                )
            else:
                self._set_default_prop_rot_dir(next_pictograph_dict, RED)

    def _set_default_prop_rot_dir(self, next_pictograph_dict, color):
        """
        Assign a random prop rotation direction for the given hand (color), unless continuous rotation is enabled.
        """
        next_pictograph_dict[color + "_attributes"]["prop_rot_dir"] = random.choice(
            ["cw", "ccw"]
        )

    def _set_default_prop_rot_dir(self, next_pictograph_dict, color):
        next_pictograph_dict[color + "_attributes"]["prop_rot_dir"] = random.choice(
            ["cw", "ccw"]
        )

    def _apply_strict_rotational_permutations(self, sequence: list[dict]) -> None:
        executor = RotationalPermutationExecuter(self.auto_builder_dialog)
        executor.create_permutations(sequence)

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
