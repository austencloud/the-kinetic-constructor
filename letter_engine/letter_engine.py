from typing import TYPE_CHECKING
from Enums.letters import Letter, LetterConditions, LetterType
from data.constants import ANTI, COUNTER_CLOCKWISE, DASH, FLOAT, PRO, CLOCKWISE
from letter_engine.non_hybrid_letter_determiner import NonHybridShiftLetterDeterminer
from objects.motion.managers.motion_ori_calculator import MotionOriCalculator
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class LetterEngine:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.letters = self.main_widget.letters
        self.non_hybrid_shift_letter_determiner = NonHybridShiftLetterDeterminer(
            main_widget, self.letters
        )

    def get_new_letter_from_motion_attributes(
        self, motion: "Motion", swap_prop_rot_dir: bool = False
    ) -> Letter:
        """Update the motion attributes based on the change in prop_rot_dir."""
        other_motion = motion.pictograph.get.other_motion(motion)
        motion_type = motion.motion_type
        if swap_prop_rot_dir:
            if motion_type == ANTI:
                new_motion_type = PRO
                motion.motion_type = new_motion_type
            elif motion_type == PRO:
                new_motion_type = ANTI
                motion.motion_type = new_motion_type
        elif motion_type == FLOAT:
            if other_motion.motion_type == FLOAT:
                letter = self.get_letter_for_dual_floats(motion)
                return letter
            new_motion_type = motion_type
            if motion.pictograph.letter in Letter.get_letters_by_condition(
                LetterConditions.TYPE1_HYBRID
            ):
                letter = self.get_lettter_for_type1_hybrids_change_to_float(motion)

                return letter
            elif motion.pictograph.letter in Letter.get_letters_by_condition(
                LetterConditions.TYPE1_NON_HYBRID
            ):
                letter = self.get_lettter_for_type1_nonhybrids_change_to_float(motion)

                return letter
        elif motion_type in [PRO, ANTI] and other_motion.motion_type == FLOAT:
            letter = self._find_matching_letter(motion)
            return letter
        elif motion_type == DASH:
            new_motion_type = motion_type
        if swap_prop_rot_dir and other_motion.motion_type == FLOAT:
            return self.non_hybrid_shift_letter_determiner.handle(motion, new_motion_type)
        # Calculate the new orientation using the MotionOriCalculator
        motion.end_ori = MotionOriCalculator(motion).get_end_ori()

        # Find the new letter based on updated attributes
        new_letter = self.find_letter_based_on_attributes(motion)
        return new_letter

    def _get_letter_for_non_hybrid_shift_swap(
        self, other_motion: "Motion", new_motion_type
    ):
        """This is for when there is one float and one shift, and the user changes the motion type of the shift.
        It ensures that we don't use hybrid letters (like C, F, I, or L) to describe letters that have one float and one pro/anti
        """

        other_motion.prefloat_motion_type = new_motion_type
        json_index = (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
            + 2
        )

        self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json(
            json_index,
            other_motion.color,
            new_motion_type,
        )
        other_motion_prefloat_prop_rot_dir = self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
            json_index, other_motion.color
        )

        if other_motion_prefloat_prop_rot_dir == COUNTER_CLOCKWISE:
            other_motion.prefloat_prop_rot_dir = CLOCKWISE
        elif other_motion_prefloat_prop_rot_dir == CLOCKWISE:
            other_motion.prefloat_prop_rot_dir = COUNTER_CLOCKWISE
        self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
            json_index,
            other_motion.color,
            other_motion.prefloat_prop_rot_dir,
        )

        for letter, examples in self.letters.items():
            for example in examples:
                if self.compare_motion_attributes_for_type1_hybrids_with_one_float(
                    other_motion, example
                ):
                    return letter

    def _update_json_with_prefloat_attributes(
        self, json_index: int, other_motion: "Motion", motion_type: str
    ) -> None:
        """Update JSON with pre-float motion type and rotation direction."""
        self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json(
            json_index,
            other_motion.color,
            motion_type,
        )

    def _get_json_index_for_current_beat(self) -> int:
        """Calculate the JSON index for the currently selected beat."""
        return (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
            + 2
        )

    def _get_prefloat_prop_rot_dir(
        self, json_index: int, other_motion: "Motion"
    ) -> str:
        """Retrieve the pre-float prop rotation direction from JSON."""
        return self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
            json_index,
            other_motion.color,
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        """Return the opposite prop rotation direction."""
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE

    def _find_matching_letter(self, motion: "Motion") -> Letter:
        """Find and return the letter that matches the motion attributes."""
        for letter, examples in self.letters.items():
            for example in examples:
                if self.compare_motion_attributes_for_type1_hybrids_with_one_float(
                    motion, example
                ):
                    return letter
        return None

    def get_letter_for_dual_floats(self, motion: "Motion"):
        """Handle the motion attributes for dual float motions."""
        other_motion = motion.pictograph.get.other_motion(motion)
        self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json(
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
            + 2,
            motion.color,
            other_motion.prefloat_motion_type,
        )
        if (
            self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == COUNTER_CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = COUNTER_CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                COUNTER_CLOCKWISE,
            )
        elif (
            self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                CLOCKWISE,
            )
        other_motion = motion.pictograph.get.other_motion(motion)

        for letter, examples in self.letters.items():
            for example in examples:
                if self.compare_motion_attributes_for_dual_floats(motion, example):
                    return letter

        return None

    def compare_motion_attributes_for_dual_floats(self, motion: "Motion", example):
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(motion, example)
            and example[f"{motion.color}_attributes"]["start_loc"] == motion.start_loc
            and example[f"{motion.color}_attributes"]["end_loc"] == motion.end_loc
            and example[f"{motion.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            and self.is_shift_motion_type_matching(
                motion.pictograph.get.other_motion(motion), example
            )
            and example[
                f"{motion.pictograph.get.other_motion(motion).color}_attributes"
            ]["start_loc"]
            == motion.pictograph.get.other_motion(motion).start_loc
            and example[
                f"{motion.pictograph.get.other_motion(motion).color}_attributes"
            ]["end_loc"]
            == motion.pictograph.get.other_motion(motion).end_loc
            and example[
                f"{motion.pictograph.get.other_motion(motion).color}_attributes"
            ]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.pictograph.get.other_motion(motion).color,
            )
        )

        return motion_attributes_match_example

    def get_lettter_for_type1_hybrids_change_to_float(self, motion: "Motion"):
        """Handle the motion attributes for type 1 hybrid motions. They should default to the letters for type1 non-hybrids."""
        # if the letter is in one of these groups, then we need to find the corresponding letter in the dataframe.
        other_motion = motion.pictograph.get.other_motion(motion)
        motion.prefloat_motion_type = other_motion.motion_type
        self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json(
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
            + 2,
            motion.color,
            other_motion.motion_type,
        )
        if (
            self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == COUNTER_CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                CLOCKWISE,
            )
        elif (
            self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = COUNTER_CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                COUNTER_CLOCKWISE,
            )
        other_motion = motion.pictograph.get.other_motion(motion)

        for letter, examples in self.letters.items():
            for example in examples:
                if self.compare_motion_attributes_for_type1_hybrids_with_one_float(
                    motion, example
                ):
                    return letter

        return None

    def get_lettter_for_type1_nonhybrids_change_to_float(self, motion: "Motion"):
        """Handle the motion attributes for type 1 non-hybrid motions. They should default to the letters for type1 non-hybrids."""
        other_motion = motion.pictograph.get.other_motion(motion)
        motion.prefloat_motion_type = (
            other_motion.motion_type
            if other_motion.motion_type != FLOAT
            else other_motion.prefloat_motion_type
        )
        self.main_widget.json_manager.updater.update_prefloat_motion_type_in_json(
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
            + 2,
            motion.color,
            other_motion.motion_type,
        )
        if (
            self.main_widget.json_manager.loader_saver.get_prop_rot_dir_from_json_at_index(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == COUNTER_CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                CLOCKWISE,
            )
        elif (
            self.main_widget.json_manager.loader_saver.get_prop_rot_dir_from_json_at_index(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
            )
            == CLOCKWISE
        ):
            motion.prefloat_prop_rot_dir = COUNTER_CLOCKWISE
            self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                motion.color,
                COUNTER_CLOCKWISE,
            )
        other_motion = motion.pictograph.get.other_motion(motion)

        for letter, examples in self.letters.items():
            for example in examples:
                if self.compare_motion_attributes_for_type1_nonhybrids_with_one_float(
                    motion, example
                ):
                    return letter

        return None

    def find_letter_based_on_attributes(self, motion: "Motion") -> str:
        """Find the letter in the dictionary that matches the given attributes for both blue and red motions."""
        # Get the other motion (opposite color)
        other_motion = motion.pictograph.get.other_motion(motion)
        letter_type = motion.pictograph.letter.get_letter_type()
        original_letter = motion.pictograph.letter
        for letter, examples in self.letters.items():

            if letter_type in [LetterType.Type2, LetterType.Type3]:
                for example in examples:
                    if self.compare_motion_attributes_for_type2_3(motion, example):
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

    def compare_motion_attributes_for_type1_hybrids_with_one_float(
        self, motion: "Motion", example
    ):
        float_motion = motion.pictograph.get.float_motion()
        non_float_motion = float_motion.pictograph.get.other_motion(float_motion)
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(float_motion, example)
            and example[f"{float_motion.color}_attributes"]["start_loc"]
            == float_motion.start_loc
            and example[f"{float_motion.color}_attributes"]["end_loc"]
            == float_motion.end_loc
            and example[f"{float_motion.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                float_motion.color,
            )
            and self.is_shift_motion_type_matching(non_float_motion, example)
            and example[f"{non_float_motion.color}_attributes"]["start_loc"]
            == non_float_motion.start_loc
            and example[f"{non_float_motion.color}_attributes"]["end_loc"]
            == non_float_motion.end_loc
            and example[f"{non_float_motion.color}_attributes"]["prop_rot_dir"]
            == non_float_motion.prop_rot_dir
        )

        return motion_attributes_match_example

    def compare_motion_attributes_for_type1_nonhybrids_with_one_float(
        self, float_motion: "Motion", example
    ):
        non_float_motion = float_motion.pictograph.get.other_motion(float_motion)
        motion_attributes_match_example = (
            self.is_shift_motion_type_matching(float_motion, example)
            and example[f"{float_motion.color}_attributes"]["start_loc"]
            == float_motion.start_loc
            and example[f"{float_motion.color}_attributes"]["end_loc"]
            == float_motion.end_loc
            and example[f"{float_motion.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self.main_widget.top_builder_widget.sequence_widget.beat_frame.get_index_of_currently_selected_beat()
                + 2,
                float_motion.color,
            )
            and self.is_shift_motion_type_matching(non_float_motion, example)
            and example[f"{non_float_motion.color}_attributes"]["start_loc"]
            == non_float_motion.start_loc
            and example[f"{non_float_motion.color}_attributes"]["end_loc"]
            == non_float_motion.end_loc
            and example[f"{non_float_motion.color}_attributes"]["prop_rot_dir"]
            == non_float_motion.prop_rot_dir
        )

        return motion_attributes_match_example

    def compare_motion_attributes_for_type2_3(self, motion: "Motion", example):
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
