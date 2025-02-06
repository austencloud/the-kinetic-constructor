from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
import random
from copy import deepcopy
from PyQt6.QtCore import Qt
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE
from ..base_classes.base_sequence_generator import BaseSequenceGenerator
from ..turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from .freeform_sequence_generator_frame import FreeformSequenceGeneratorFrame


class FreeFormSequenceGenerator(BaseSequenceGenerator):
    def __init__(self, sequence_generator_frame: "FreeformSequenceGeneratorFrame"):
        super().__init__(sequence_generator_frame)
        self.sequence_generator_frame = sequence_generator_frame

    def build_sequence(
        self,
        length: int,
        turn_intensity: int,
        level: int,
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

        turn_manager = TurnIntensityManager(length, level, turn_intensity)
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()

        for i in range(length - length_of_sequence_upon_start):
            next_pictograph = self._generate_next_pictograph(
                level,
                turns_blue[i],
                turns_red[i],
                is_continuous_rot_dir,
                blue_rot_dir,
                red_rot_dir,
            )
            self.sequence.append(next_pictograph)
            self.sequence_widget.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                next_pictograph, override_grow_sequence=True
            )
            QApplication.processEvents()

        construct_tab = self.main_widget.construct_tab
        construct_tab.option_picker.update_option_picker(self.sequence)

        QApplication.restoreOverrideCursor()

    def _generate_next_pictograph(
        self,
        level: int,
        turn_blue: float,
        turn_red: float,
        is_continuous_rot_dir: bool,
        blue_rot_dir: str,
        red_rot_dir: str,
    ):

        option_dicts = self.main_widget.construct_tab.option_picker.option_getter._load_all_next_option_dicts(
            self.sequence
        )
        option_dicts = [deepcopy(option) for option in option_dicts]

        option_dicts = self._filter_options_by_letter_type(option_dicts)

        if is_continuous_rot_dir:
            option_dicts = self._filter_options_by_rotation(
                option_dicts, blue_rot_dir, red_rot_dir
            )

        last_beat = self.sequence[-1]
        next_beat = random.choice(option_dicts)

        if level == 2 or level == 3:
            next_beat = self._set_turns(next_beat, turn_blue, turn_red)

        self._update_start_oris(next_beat, last_beat)
        self._update_end_oris(next_beat)
        self._update_dash_static_prop_rot_dirs(
            next_beat, is_continuous_rot_dir, blue_rot_dir, red_rot_dir
        )
        next_beat = self._update_beat_number_depending_on_sequence_length(
            next_beat, self.sequence
        )
        return next_beat

    def _filter_options_by_letter_type(self, options: list[dict]) -> list[dict]:
        """Filter options based on selected letter types."""
        selected_types = self.sequence_generator_frame.get_selected_letter_types()
        selected_letters = []
        for letter_type in selected_types:
            selected_letters.extend(letter_type.letters)

        filtered_options = [
            option for option in options if option["letter"] in selected_letters
        ]
        return filtered_options
