from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
import random
from copy import deepcopy
from PyQt6.QtCore import Qt
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE
from data.position_maps import (
    half_position_map,
    quarter_position_map_cw,
    quarter_position_map_ccw,
)
from data.quartered_permutations import quartered_permutations
from data.halved_permutations import halved_permutations
from ..base_classes.base_sequence_generator import BaseSequenceGenerator
from .permutation_executors.mirrored_permutation_executor import (
    MirroredPermutationExecutor,
)
from .permutation_executors.rotated_permutation_executor import (
    RotatedPermutationExecuter,
)
from ..turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from .circular_sequence_generator_frame import CircularSequenceGeneratorFrame


class CircularSequenceGenerator(BaseSequenceGenerator):
    def __init__(self, sequence_generator_frame: "CircularSequenceGeneratorFrame"):
        super().__init__(sequence_generator_frame)
        self.rotated_executor = RotatedPermutationExecuter(self)
        self.mirrored_executor = MirroredPermutationExecutor(self, False)

    def build_sequence(
        self,
        length: int,
        turn_intensity: int,
        level: int,
        rotation_type: str,
        permutation_type: str,
        is_continuous_rot_dir: bool,
    ):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self._initialize_sequence(length)

        if is_continuous_rot_dir:
            blue_rot_dir = random.choice([CLOCKWISE, COUNTER_CLOCKWISE])
            red_rot_dir = random.choice([CLOCKWISE, COUNTER_CLOCKWISE])
        else:
            blue_rot_dir = None
            red_rot_dir = None

        length_of_sequence_upon_start = len(self.sequence) - 2

        if permutation_type == "rotated":
            if rotation_type == "quartered":
                word_length = length // 4
            elif rotation_type == "halved":
                word_length = length // 2
            available_range = word_length - length_of_sequence_upon_start
        elif permutation_type == "mirrored":
            word_length = length // 2
            available_range = word_length - length_of_sequence_upon_start

        turn_manager = TurnIntensityManager(word_length, level, turn_intensity)
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()

        for i in range(available_range):
            is_last_in_word = i == word_length - length_of_sequence_upon_start - 1
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

            self.sequence.append(next_pictograph)
            self.sequence_widget.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            QApplication.processEvents()

        self._apply_permutations(self.sequence, permutation_type, rotation_type)
        
        construct_tab = self.main_widget.construct_tab
        construct_tab.option_picker.update_option_picker(self.sequence)
        
        QApplication.restoreOverrideCursor()

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
        options = self.main_widget.construct_tab.option_picker.option_getter._load_all_next_option_dicts(
            self.sequence
        )
        options = [deepcopy(option) for option in options]

        if is_continuous_rot_dir:
            options = self._filter_options_by_rotation(
                options, blue_rot_dir, red_rot_dir
            )
        if permutation_type == "rotated":
            if is_last_in_word:
                expected_end_pos = self._determine_rotated_end_pos(rotation_type)
                next_beat = self._select_pictograph_with_end_pos(
                    options, expected_end_pos
                )
            else:
                next_beat = random.choice(options)

        elif permutation_type == "mirrored":
            if is_last_in_word:
                expected_end_pos = self.sequence[1]["end_pos"]
                next_beat = self._select_pictograph_with_end_pos(
                    options, expected_end_pos
                )
            else:
                next_beat = random.choice(options)

        if level == 2 or level == 3:
            next_beat = self._set_turns(next_beat, turn_blue, turn_red)

        self._update_start_oris(next_beat, self.sequence[-1])
        self._update_end_oris(next_beat)
        self._update_dash_static_prop_rot_dirs(
            next_beat,
            is_continuous_rot_dir,
            blue_rot_dir,
            red_rot_dir,
        )
        next_beat = self._update_beat_number_depending_on_sequence_length(
            next_beat, self.sequence
        )
        return next_beat

    def _determine_rotated_end_pos(self, rotation_type: str) -> str:
        """Determine the expected end position based on rotation type and current sequence."""
        start_pos = self.sequence[1]["end_pos"]

        if rotation_type == "quartered":
            if random.choice([True, False]):
                return quarter_position_map_cw[start_pos]
            else:
                return quarter_position_map_ccw[start_pos]
        elif rotation_type == "halved":
            return half_position_map[start_pos]
        else:
            print("Invalid rotation type - expected 'quartered' or 'halved'")
            return None

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

    def _apply_permutations(
        self, sequence: list[dict], permutation_type: str, rotation_type: str
    ) -> None:
        if permutation_type == "rotated":
            if self.can_perform_rotationed_permutation(sequence, rotation_type):
                self.rotated_executor.create_permutations(sequence)
        elif permutation_type == "mirrored":
            if self.mirrored_executor.can_perform_mirrored_permutation(sequence):
                self.mirrored_executor.create_permutations(sequence, "vertical")

    def can_perform_rotationed_permutation(
        self, sequence: list[dict], rotation_type: str
    ) -> bool:
        start_pos = sequence[1]["end_pos"]
        end_pos = sequence[-1]["end_pos"]
        if rotation_type == "quartered":
            return (start_pos, end_pos) in quartered_permutations
        elif rotation_type == "halved":
            return (start_pos, end_pos) in halved_permutations
