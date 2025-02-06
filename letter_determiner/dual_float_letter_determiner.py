from typing import TYPE_CHECKING
from Enums.letters import Letter
from data.constants import COUNTER_CLOCKWISE, CLOCKWISE

if TYPE_CHECKING:
    from .letter_determiner import LetterDeterminer
    from main_window.main_widget.main_widget import MainWidget
    from objects.motion.motion import Motion


class DualFloatLetterDeterminer:
    def __init__(self, letter_engine: "LetterDeterminer"):
        self.main_widget = letter_engine.main_widget
        self.letters = letter_engine.letters

    def determine_letter(self, motion: "Motion") -> Letter:
        """Handle the motion attributes for dual float motions."""
        other_motion = motion.pictograph.get.other_motion(motion)
        self._update_prefloat_attributes(motion, other_motion)
        return self._find_matching_letter(motion)

    def _update_prefloat_attributes(
        self, motion: "Motion", other_motion: "Motion"
    ) -> None:
        json_index = self._get_json_index_for_current_beat()
        self._update_json_with_prefloat_attributes(
            json_index, motion.color, other_motion.prefloat_motion_type
        )
        motion.prefloat_prop_rot_dir = self._get_prefloat_prop_rot_dir(
            json_index, motion
        )

        self.main_widget.json_manager.updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
            json_index, motion.color, motion.prefloat_prop_rot_dir
        )

    def _get_json_index_for_current_beat(self) -> int:
        return (
            self.main_widget.sequence_widget.beat_frame.get.index_of_currently_selected_beat()
            + 2
        )

    def _update_json_with_prefloat_attributes(
        self, json_index: int, color: str, motion_type: str
    ) -> None:
        self.main_widget.json_manager.updater.motion_type_updater.update_prefloat_motion_type_in_json(
            json_index, color, motion_type
        )

    def _get_prefloat_prop_rot_dir(self, json_index: int, motion: "Motion") -> str:
        return self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
            json_index, motion.color
        )

    def _get_opposite_rotation_direction(self, rotation_direction: str) -> str:
        return COUNTER_CLOCKWISE if rotation_direction == CLOCKWISE else CLOCKWISE

    def _find_matching_letter(self, motion: "Motion") -> Letter:
        for letter, examples in self.letters.items():
            for example in examples:
                if self._compare_motion_attributes(motion, example):
                    return letter
        return None

    def _compare_motion_attributes(self, motion: "Motion", example) -> bool:
        other_motion = motion.pictograph.get.other_motion(motion)
        return (
            example[f"{motion.color}_attributes"]["start_loc"] == motion.start_loc
            and example[f"{motion.color}_attributes"]["end_loc"] == motion.end_loc
            and example[f"{motion.color}_attributes"]["prop_rot_dir"]
            == motion.prefloat_prop_rot_dir
            and example[f"{other_motion.color}_attributes"]["start_loc"]
            == other_motion.start_loc
            and example[f"{other_motion.color}_attributes"]["end_loc"]
            == other_motion.end_loc
            and example[f"{other_motion.color}_attributes"]["prop_rot_dir"]
            == self.main_widget.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                self._get_json_index_for_current_beat(), other_motion.color
            )
        )
