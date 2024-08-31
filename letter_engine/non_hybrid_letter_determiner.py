from typing import TYPE_CHECKING
from Enums.letters import Letter
from data.constants import COUNTER_CLOCKWISE, CLOCKWISE

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from objects.motion.motion import Motion


class NonHybridShiftLetterDeterminer:
    def __init__(self, main_widget: "MainWidget", letters: dict) -> None:
        self.main_widget = main_widget
        self.letters = letters

    def handle(self, motion: "Motion", new_motion_type: str) -> Letter:
        """Handle the case where there is one float and one shift, and the user changes the motion type of the shift."""
        other_motion = motion.pictograph.get.other_motion(motion)
        self._update_motion_attributes(other_motion, new_motion_type)
        return self._find_matching_letter(motion)

    def _update_motion_attributes(
        self, other_motion: "Motion", new_motion_type: str
    ) -> None:
        """Update the attributes of the other motion."""
        other_motion.prefloat_motion_type = new_motion_type
        json_index = self._get_json_index_for_current_beat()

        self._update_json_with_prefloat_attributes(
            json_index, other_motion, new_motion_type
        )

        prefloat_prop_rot_dir = self._get_prefloat_prop_rot_dir(
            json_index, other_motion
        )
        other_motion.prefloat_prop_rot_dir = self._get_opposite_rotation_direction(
            prefloat_prop_rot_dir
        )

        self.main_widget.json_manager.updater.update_prefloat_prop_rot_dir_in_json(
            json_index,
            other_motion.color,
            other_motion.prefloat_prop_rot_dir,
        )

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
                if self._compare_motion_attributes(motion, example):
                    return letter
        return None

    def _compare_motion_attributes(self, motion: "Motion", example) -> bool:
        """Compare the motion attributes with the example to find a match."""
        float_motion = motion.pictograph.get.float_motion()
        non_float_motion = float_motion.pictograph.get.other_motion(float_motion)

        return (
            self._is_shift_motion_type_matching(float_motion, example)
            and example[f"{float_motion.color}_attributes"]["start_loc"]
            == float_motion.start_loc
            and example[f"{float_motion.color}_attributes"]["end_loc"]
            == float_motion.end_loc
            and example[f"{float_motion.color}_attributes"]["prop_rot_dir"]
            == self._get_prefloat_prop_rot_dir(
                self._get_json_index_for_current_beat(), float_motion
            )
            and self._is_shift_motion_type_matching(non_float_motion, example)
            and example[f"{non_float_motion.color}_attributes"]["start_loc"]
            == non_float_motion.start_loc
            and example[f"{non_float_motion.color}_attributes"]["end_loc"]
            == non_float_motion.end_loc
            and example[f"{non_float_motion.color}_attributes"]["prop_rot_dir"]
            == non_float_motion.prop_rot_dir
        )

    def _is_shift_motion_type_matching(self, motion: "Motion", example) -> bool:
        """Check if the motion type matches."""
        return (
            example[f"{motion.color}_attributes"]["motion_type"] == motion.motion_type
            or example[f"{motion.color}_attributes"]["motion_type"]
            == motion.prefloat_motion_type
        )
