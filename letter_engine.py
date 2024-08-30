from typing import TYPE_CHECKING
from Enums.letters import Letter, LetterType
from data.constants import ANTI, COUNTER_CLOCKWISE, FLOAT, PRO, CLOCKWISE
from objects.motion.managers.motion_ori_calculator import MotionOriCalculator
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterEngine:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.letters

    def update_motion_attributes(
        self, motion: "Motion", prop_rot_dir: str
    ) -> tuple[Letter, "Motion"]:
        """Update the motion attributes based on the change in prop_rot_dir."""
        other_motion = motion.pictograph.get.other_motion(motion)
        motion_type = motion.motion_type
        if motion_type == ANTI:
            new_motion_type = PRO
        elif motion_type == PRO:
            new_motion_type = ANTI
        else:
            new_motion_type = motion_type
        if other_motion.motion_type == FLOAT:
            other_motion.prefloat_motion_type = new_motion_type
            json_index = (
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2
            )

            self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json_at_index(
                json_index,
                other_motion.color,
                new_motion_type,
            )
            other_motion_prefloat_prop_rot_dir = self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json_at_index(
                json_index, other_motion.color
            )

            if other_motion_prefloat_prop_rot_dir == COUNTER_CLOCKWISE:
                other_motion.prefloat_prop_rot_dir = CLOCKWISE
            elif other_motion_prefloat_prop_rot_dir == CLOCKWISE:
                other_motion.prefloat_prop_rot_dir = COUNTER_CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json_at_index(
                json_index,
                other_motion.color,
                other_motion.prefloat_prop_rot_dir,
            )

        motion.motion_type = new_motion_type
        motion.prop_rot_dir = prop_rot_dir

        # Calculate the new orientation using the MotionOriCalculator
        motion.end_ori = MotionOriCalculator(motion).get_end_ori()

        # Find the new letter based on updated attributes
        new_letter = self.find_letter_based_on_attributes(motion)
        return new_letter, motion

    def find_letter_based_on_attributes(self, motion: "Motion") -> str:
        """Find the letter in the dictionary that matches the given attributes for both blue and red motions."""
        # Get the other motion (opposite color)
        other_motion = motion.pictograph.get.other_motion(motion)
        letter_type = motion.pictograph.letter.get_letter_type()
        original_letter = motion.pictograph.letter
        for letter, examples in self.letters.items():

            if letter_type in [LetterType.Type2, LetterType.Type3]:
                for example in examples:
                    if self.compare_motion_attributes_for_type2_3(
                        motion, other_motion, example
                    ):
                        return letter
            elif letter_type == LetterType.Type1:
                for example in examples:
                    if self.compare_motion_attributes_for_type1(
                        motion, other_motion, example
                    ):
                        return letter
            else:
                return original_letter
        return None

    def compare_motion_attributes_for_type1(
        self, motion: "Motion", other_motion: "Motion", example
    ):
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(motion, example)
            and example[f"{motion.color}_attributes"]["start_loc"] == motion.start_loc
            and example[f"{motion.color}_attributes"]["end_loc"] == motion.end_loc
            and example[f"{motion.color}_attributes"]["prop_rot_dir"]
            == motion.prop_rot_dir
            and self.is_shift_motion_type_matching(other_motion, example)
            and example[f"{other_motion.color}_attributes"]["start_loc"]
            == other_motion.start_loc
            and example[f"{other_motion.color}_attributes"]["end_loc"]
            == other_motion.end_loc
            and example[f"{other_motion.color}_attributes"]["prop_rot_dir"]
            == other_motion.prop_rot_dir
        )

        return motion_attributes_match_example

    def compare_motion_attributes_for_type2_3(
        self, motion: "Motion", other_motion: "Motion", example
    ):
        shift = motion.pictograph.get.shift()
        non_shift = motion.pictograph.get.other_motion(shift)
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(shift, example)
            and example[f"{shift.color}_attributes"]["start_loc"] == shift.start_loc
            and example[f"{shift.color}_attributes"]["end_loc"] == shift.end_loc
            and example[f"{shift.color}_attributes"]["prop_rot_dir"]
            == shift.prop_rot_dir
            and example[f"{non_shift.color}_attributes"]["motion_type"]
            == non_shift.motion_type
            and example[f"{non_shift.color}_attributes"]["start_loc"]
            == non_shift.start_loc
            and example[f"{non_shift.color}_attributes"]["end_loc"] == non_shift.end_loc
        )

        return motion_attributes_match_example

    def is_shift_motion_type_matching(self, motion: "Motion", example):
        is_matching_motion_type = (
            example[f"{motion.color}_attributes"]["motion_type"] == motion.motion_type
            or example[f"{motion.color}_attributes"]["motion_type"]
            == motion.prefloat_motion_type
        )

        return is_matching_motion_type
