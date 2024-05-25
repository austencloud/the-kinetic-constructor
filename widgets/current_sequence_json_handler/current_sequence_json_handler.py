import json
from Enums.MotionAttributes import Color
from Enums.PropTypes import PropType
from circular_word_checker import CircularWordChecker
from constants import BLUE, DASH, NO_ROT, RED, STATIC
from path_helpers import get_user_editable_resource_path
from widgets.sequence_widget.SW_beat_frame.beat import BeatView
from .motion_orientation_json_calculator import CurrentSequenceJsonOriCalculator
from widgets.pictograph.pictograph import Pictograph
from typing import TYPE_CHECKING, Union

from sequence_validation_engine import (
    SequenceValidationEngine,
)

if TYPE_CHECKING:
    from widgets.json_manager import JSON_Manager


class CurrentSequenceJsonHandler:
    def __init__(self, json_manager: "JSON_Manager") -> None:
        self.main_widget = json_manager.main_widget

        self.current_sequence_json = get_user_editable_resource_path(
            "current_sequence.json"
        )

        self.ori_calculator = CurrentSequenceJsonOriCalculator(self)
        self.validation_engine = SequenceValidationEngine(self)

        self.clear_current_sequence_file()  # Clears or initializes the file at the new location

    def update_sequence_properties(self):
        sequence = self.load_current_sequence_json()
        if len(sequence) > 1:
            checker = CircularWordChecker(
                sequence[1:]
            )  # Passing the sequence entries after metadata
            is_circular, is_permutable = checker.check_properties()
            sequence[0]["is_circular"] = is_circular
            sequence[0]["is_permutable"] = is_permutable
            self.save_current_sequence(sequence)

    def update_prop_type_in_json(self, prop_type: PropType) -> None:
        sequence = self.load_current_sequence_json()
        sequence[0]["prop_type"] = prop_type.name.lower()
        self.save_current_sequence(sequence)

    def set_start_position_data(self, start_pos_pictograph: Pictograph) -> None:
        red_start_ori = start_pos_pictograph.pictograph_dict["red_attributes"][
            "start_ori"
        ]
        blue_start_ori = start_pos_pictograph.pictograph_dict["blue_attributes"][
            "start_ori"
        ]

        self.sequence = self.load_current_sequence_json()

        start_position_dict = {
            "sequence_start_position": start_pos_pictograph.end_pos[:-1],
            "letter": start_pos_pictograph.letter.name,
            "end_pos": start_pos_pictograph.end_pos,
            "blue_attributes": {
                "start_loc": start_pos_pictograph.blue_motion.start_loc,
                "end_loc": start_pos_pictograph.blue_motion.end_loc,
                "start_ori": blue_start_ori,
                "end_ori": blue_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.blue_motion.motion_type,
            },
            "red_attributes": {
                "start_loc": start_pos_pictograph.red_motion.start_loc,
                "end_loc": start_pos_pictograph.red_motion.end_loc,
                "start_ori": red_start_ori,
                "end_ori": red_start_ori,
                "prop_rot_dir": NO_ROT,
                "turns": 0,
                "motion_type": start_pos_pictograph.red_motion.motion_type,
            },
        }

        if len(self.sequence) == 1:
            self.sequence.append(start_position_dict)
        else:
            self.sequence.insert(1, start_position_dict)

        self.save_current_sequence(self.sequence)

    def load_current_sequence_json(self) -> list:
        try:
            with open(self.current_sequence_json, "r", encoding="utf-8") as file:
                sequence = json.load(file)
            return sequence
        except FileNotFoundError:
            print("Current sequence json not found")
            return [
                {
                    "prop_type": self.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                }
            ]

    def save_current_sequence(self, sequence):
        if not sequence:
            sequence = [
                {
                    "prop_type": self.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                    "is_permutable": False,
                }
            ]
        else:
            if "prop_type" not in sequence[0]:
                sequence[0]["prop_type"] = self.main_widget.prop_type.name.lower()
            if "is_circular" not in sequence[0]:
                sequence[0]["is_circular"] = False
            if "is_permutable" not in sequence[0]:
                sequence[0]["is_permutable"] = False
        with open(self.current_sequence_json, "w", encoding="utf-8") as file:
            json.dump(sequence, file, indent=4, ensure_ascii=False)

    def get_red_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["red_attributes"]["end_ori"]
        return 0

    def get_blue_end_ori(self, sequence):
        if sequence:
            return sequence[-1]["blue_attributes"]["end_ori"]
        return 0

    def clear_current_sequence_file(self):
        with open(self.current_sequence_json, "w", encoding="utf-8") as file:
            json.dump(
                [
                    {
                        "prop_type": self.main_widget.prop_type.name.lower(),
                        "is_circular": False,
                        "is_permutable": False,
                    }
                ],
                file,
                indent=4,
            )

    def update_current_sequence_file_with_beat(self, beat_view: BeatView):
        sequence_data = self.load_current_sequence_json()
        if len(sequence_data) == 0:  # Make sure there's at least the metadata entry
            sequence_data.append(
                {
                    "prop_type": self.main_widget.prop_type.name.lower(),
                    "is_circular": False,
                }
            )
        sequence_data.append(beat_view.beat.pictograph_dict)
        self.save_current_sequence(sequence_data)
        self.update_sequence_properties()  # Recalculate circularity after each update

    def clear_and_repopulate_the_current_sequence(self):
        self.clear_current_sequence_file()
        beat_frame = self.main_widget.top_builder_widget.sequence_widget.beat_frame
        beat_views = beat_frame.beats
        start_pos = beat_frame.start_pos_view.start_pos
        if start_pos.view.is_filled:
            self.set_start_position_data(start_pos)
        for beat_view in beat_views:
            if beat_view.is_filled:
                self.update_current_sequence_file_with_beat(beat_view)

    def get_index_for_pictograph(self, pictograph: Pictograph):
        sequence = self.load_current_sequence_json()
        for i, entry in enumerate(sequence):
            if entry == pictograph.pictograph_dict:
                return i
        return -1

    def update_turns_in_json_at_index(
        self, index: int, color: Color, turns: Union[int, float]
    ) -> None:
        sequence = self.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.ori_calculator.calculate_end_orientation(sequence[index], color)
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori

        if sequence[index][f"{color}_attributes"]["turns"] > 0:
            pictograph = (
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                    index - 2
                ].blank_beat
            )
            if pictograph:
                motion = pictograph.get.motion_by_color(color)
                prop_rot_dir = motion.prop_rot_dir
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        if sequence[index][f"{color}_attributes"]["motion_type"] in [DASH, STATIC]:
            if sequence[index][f"{color}_attributes"]["turns"] == 0:
                prop_rot_dir = NO_ROT
                sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir

        self.save_current_sequence(sequence)

    def update_start_pos_ori(self, color: Color, ori: int) -> None:
        sequence = self.load_current_sequence_json()
        if sequence:
            sequence[1][f"{color}_attributes"]["end_ori"] = ori
            sequence[1][f"{color}_attributes"]["start_ori"] = ori
            self.save_current_sequence(sequence)

    def update_rot_dir_in_json_at_index(
        self, index: int, color: Color, prop_rot_dir: str
    ) -> None:
        sequence = self.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["prop_rot_dir"] = prop_rot_dir
        self.save_current_sequence(sequence)

    def apply_turn_pattern_to_current_sequence(self, pattern: list[tuple]) -> None:
        sequence = self.load_current_sequence_json()
        min_length = min(len(sequence), len(pattern))
        for i in range(1, min_length + 1):
            if i == 17:
                continue
            blue_turns, red_turns = pattern[i - 1]
            blue_turns = int(blue_turns) if blue_turns.is_integer() else blue_turns
            red_turns = int(red_turns) if red_turns.is_integer() else red_turns

            if i >= len(sequence):
                break

            entry = sequence[i]
            entry["blue_attributes"]["turns"] = blue_turns
            entry["red_attributes"]["turns"] = red_turns

            if entry["blue_attributes"]["motion_type"] in [STATIC, DASH]:
                if not blue_turns == 0:
                    entry["blue_attributes"]["prop_rot_dir"] = (
                        self._calculate_continuous_prop_rot_dir(sequence, i, BLUE)
                    )
            if entry["red_attributes"]["motion_type"] in [STATIC, DASH]:
                if not red_turns == 0:
                    entry["red_attributes"]["prop_rot_dir"] = (
                        self._calculate_continuous_prop_rot_dir(sequence, i, RED)
                    )

            beat_view = (
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.beats[
                    i - 1
                ]
            )
            if beat_view and beat_view.is_filled:
                beat_view.blank_beat.get.pictograph_dict().update(entry)

        self.save_current_sequence(sequence)
        self.validation_engine.run(is_current_sequence=True)
        sequence = self.load_current_sequence_json()
        self.main_widget.top_builder_widget.sequence_widget.beat_frame.propogate_turn_adjustment(
            sequence
        )

    def _calculate_continuous_prop_rot_dir(self, sequence, current_index, color) -> str:
        ignore_motion_types = [STATIC, DASH]

        for i in range(current_index - 1, max(current_index - 16, -1), -1):
            if i == 0:
                continue
            if (
                sequence[i][f"{color}_attributes"]["motion_type"]
                not in ignore_motion_types
            ):
                return sequence[i][f"{color}_attributes"]["prop_rot_dir"]

        return NO_ROT
