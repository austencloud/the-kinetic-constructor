from typing import TYPE_CHECKING, Union
from data.constants import DASH, STATIC, NO_ROT, FLOAT

if TYPE_CHECKING:
    from main_window.main_widget.json_manager.json_sequence_updater.json_sequence_updater import (
        JsonSequenceUpdater,
    )
    from objects.motion.motion import Motion


class JsonTurnsUpdater:
    def __init__(self, json_updater: "JsonSequenceUpdater"):
        self.json_updater = json_updater
        self.json_manager = json_updater.json_manager
        self.main_widget = self.json_manager.main_widget

    def update_turns_in_json(
        self, motion: "Motion", new_turns: Union[int, float]
    ) -> None:
        """Update the turns value in JSON for the given motion."""
        beat_index = self._get_json_index()
        self.update_turns_in_json_at_index(beat_index, motion.color, new_turns)
        self.update_motion_type_in_json(motion, beat_index, new_turns)
        self.update_prop_rot_dir_in_json(motion, beat_index, new_turns)

    def update_turns_in_json_at_index(
        self, index: int, color: str, turns: Union[int, float]
    ) -> None:
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        sequence[index][f"{color}_attributes"]["turns"] = turns
        end_ori = self.json_manager.ori_calculator.calculate_end_ori(
            sequence[index], color
        )
        sequence[index][f"{color}_attributes"]["end_ori"] = end_ori

        if turns == "fl":
            self._handle_float_turn_cleanup(sequence, index, color)
        else:
            self._handle_non_float_turn_updates(sequence, index, color, turns)

        self.json_manager.loader_saver.save_current_sequence(sequence)
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def update_motion_type_in_json(
        self, motion: "Motion", index: int, new_turns: Union[int, float]
    ) -> None:
        if new_turns == "fl":
            self.json_updater.motion_type_updater.update_prefloat_motion_type_in_json(
                index, motion.color, motion.motion_type
            )
            motion.motion_type = FLOAT
        else:
            motion.motion_type = (
                self.json_manager.loader_saver.get_prefloat_motion_type_from_json_at_index(
                    index, motion.color
                )
                if motion.motion_type == FLOAT
                else motion.motion_type
            )
        self.json_updater.motion_type_updater.update_motion_type_in_json_at_index(
            index, motion.color, motion.motion_type
        )

    def update_prop_rot_dir_in_json(
        self, motion: "Motion", index: int, new_turns: Union[int, float]
    ) -> None:
        if motion.motion_type in [DASH, STATIC] and new_turns == 0:
            motion.prop_rot_dir = NO_ROT
        elif new_turns == "fl":
            motion.prop_rot_dir = NO_ROT
            self.json_updater.prop_rot_dir_updater.update_prefloat_prop_rot_dir_in_json(
                index, motion.color, motion.prop_rot_dir
            )
        else:
            motion.prop_rot_dir = (
                self.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                    index, motion.color
                )
                if motion.motion_type == FLOAT
                else motion.prop_rot_dir
            )
        self.json_updater.prop_rot_dir_updater.update_prop_rot_dir_in_json_at_index(
            index, motion.color, motion.prop_rot_dir
        )

    def _handle_float_turn_cleanup(self, sequence, index: int, color: str) -> None:
        """Remove non-relevant fields when turns are 'float'."""
        attributes = sequence[index][f"{color}_attributes"]
        if "prefloat_prop_rot_dir" in attributes:
            del attributes["prefloat_prop_rot_dir"]

    def _handle_non_float_turn_updates(
        self, sequence, index: int, color: str, turns: Union[int, float]
    ) -> None:
        """Add or update properties when turns are not 'float'."""
        attributes = sequence[index][f"{color}_attributes"]
        if "prop_rot_dir" not in attributes:
            attributes["prop_rot_dir"] = NO_ROT

    def _get_json_index(self) -> int:
        """Get the JSON index of the currently selected beat."""
        beat_index = (
            self.main_widget.sequence_widget.beat_frame.get.index_of_currently_selected_beat()
        )
        return beat_index + 2
