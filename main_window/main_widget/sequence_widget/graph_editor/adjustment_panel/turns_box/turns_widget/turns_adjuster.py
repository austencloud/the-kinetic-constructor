from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
from Enums.Enums import Turns
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    FLOAT,
    NO_ROT,
    STATIC,
)
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class TurnsAdjustmentManager(QObject):
    turns_adjusted = pyqtSignal(object)  # Signal can now handle any type

    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.graph_editor = self.turns_widget.turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
        self.main_widget = self.graph_editor.main_widget
        self.json_manager = self.main_widget.json_manager
        self.json_validation_engine = self.json_manager.ori_validation_engine
        self.color = self.turns_widget.turns_box.color
        self.turns_box = self.turns_widget.turns_box
        self.prop_rot_dir_manager = self.turns_box.prop_rot_dir_button_manager
        self.turns_adjusted.connect(
            self.beat_frame.updater.update_beats_from_current_sequence_json
        )

    def adjust_turns(self, adjustment: Union[int, float]) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        GE_view = self.graph_editor.pictograph_container.GE_view
        self.GE_pictograph = GE_view.pictograph
        self.reference_beat = GE_view.reference_beat

        current_turns = self._get_turns()
        matching_motion = self.reference_beat.motions[self.color]

        if current_turns == "fl" and adjustment > 0:
            new_turns = 0
        elif current_turns == "fl" and adjustment < 0:
            QApplication.restoreOverrideCursor()
            return
        elif current_turns == 0 and adjustment < 0:
            new_turns = "fl"
        else:
            new_turns = self._clamp_turns(current_turns + adjustment)
            new_turns = self.convert_turn_floats_to_ints(new_turns)
            
        self._update_motion_properties(new_turns)

        self.turns_widget.display_frame.update_turns_display(matching_motion, new_turns)

        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.main_widget.construct_tab.option_picker.update_option_picker()
        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        self.beat_frame.updater.update_beats_from(sequence)
        QApplication.restoreOverrideCursor()

    def get_new_letter(self, new_turns, motion):
        need_to_determine_new_letter: bool = self.determine_if_new_letter_is_needed(
            motion, new_turns
        )
        if need_to_determine_new_letter:
            new_letter = self.main_widget.letter_determiner.determine_letter(motion)
        else:
            new_letter = None
        return new_letter

    def determine_if_new_letter_is_needed(self, motion: Motion, new_turns) -> bool:
        if new_turns == "fl":
            return True
        if motion.turns == "fl" and new_turns >= 0:
            return True
        return False

    def direct_set_turns(self, new_turns: Turns) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        GE_view = self.graph_editor.pictograph_container.GE_view
        self.GE_pictograph = GE_view.pictograph
        self.reference_beat = GE_view.reference_beat
        self._update_motion_properties(new_turns)

        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns
        )
        self.reference_beat.motions[self.color].turns = new_turns
        self.turns_widget.display_frame.update_turns_display(
            self.reference_beat.motions[self.color], new_turns
        )

        pictographs: list[BasePictograph] = [self.reference_beat, self.GE_pictograph]
        for pictograph in pictographs:
            for motion in pictograph.motions.values():
                if motion.color == self.turns_box.color:
                    self.set_motion_turns(motion, new_turns)

        matching_motion = self.reference_beat.motions[self.color]
        GE_motion = self.GE_pictograph.motions[self.color]

        for motion in [matching_motion, GE_motion]:
            motion.turns = new_turns
            self.turns_widget.turns_box.prop_rot_dir_button_manager._update_pictograph_and_json(
                motion
            )

        self.json_validation_engine.run(is_current_sequence=True)
        self.main_widget.construct_tab.option_picker.update_option_picker()
        self.turns_adjusted.emit(new_turns)
        QApplication.restoreOverrideCursor()

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.display_frame.turns_label.text()
        if turns == "fl":
            return "fl"
        turns = self.convert_turns_from_str_to_num(turns)
        turns = self.convert_turn_floats_to_ints(turns)
        return turns

    def convert_turns_from_str_to_num(self, turns) -> Union[int, float]:
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)

    def convert_turn_floats_to_ints(self, turns: Turns) -> Turns:
        if turns in [0.0, 1.0, 2.0, 3.0]:
            return int(turns)
        else:
            return turns

    def _clamp_turns(self, turns: Turns) -> Turns:
        if isinstance(turns, (int, float)):
            return max(0, min(3, turns))
        return turns

    def _update_turns_display(self, turns: Turns) -> None:
        self.turns_widget.display_frame.update_turns_display(turns)

    def _update_motion_properties(self, new_turns) -> None:
        for motion in [
            self.reference_beat.motions[self.color],
            self.GE_pictograph.motions[self.color],
        ]:
            self.set_motion_turns(motion, new_turns)
            if new_turns == 0 and motion.motion_type in [DASH, STATIC]:
                motion.prop_rot_dir = NO_ROT
            elif new_turns == "fl":
                motion.motion_type = FLOAT
                motion.prop_rot_dir = NO_ROT

            self.prop_rot_dir_manager.update_prop_rotation_buttons(motion, new_turns)
            motion.turns_manager.set_motion_turns(new_turns)
            self.turns_box.header.update_turns_box_header()
            beat_index = self._calculate_beat_index()

            if motion.turns == "fl" and new_turns != "fl":
                self._restore_motion_from_prefloat(motion, beat_index)

    def _calculate_beat_index(self) -> int:
        """Calculate the beat index for JSON updates."""
        current_beat = self.beat_frame.get.beat_number_of_currently_selected_beat()
        duration = self.beat_frame.get.duration_of_currently_selected_beat()
        return current_beat + duration

    def _get_motion_type_from_json(self, index: int, color: str) -> int:
        """Retrieve motion type from JSON at the given index."""
        return self.json_manager.loader_saver.get_motion_type_from_json_at_index(
            index, color
        )

    def _get_prop_rot_dir_from_json(self, index: int, color: str) -> int:
        """Retrieve prop rotation direction from JSON at the given index."""
        return self.json_manager.loader_saver.get_prop_rot_dir_from_json(index, color)

    def _restore_motion_from_prefloat(self, motion: "Motion", beat_index: int) -> None:
        """Restore motion properties from prefloat values."""
        motion.prefloat_motion_type = (
            self.json_manager.loader_saver.get_prefloat_motion_type_from_json_at_index(
                beat_index, motion.color
            )
        )
        motion.prefloat_prop_rot_dir = (
            self.json_manager.loader_saver.get_prefloat_prop_rot_dir_from_json(
                beat_index, motion.color
            )
        )
        motion.motion_type = motion.prefloat_motion_type
        motion.prop_rot_dir = motion.prefloat_prop_rot_dir

    def _set_prop_rot_dir_state_default(self) -> None:
        """Set the prop rotation direction state to clockwise by default."""
        self.turns_box.prop_rot_dir_btn_state[CLOCKWISE] = True
        self.turns_box.prop_rot_dir_btn_state[COUNTER_CLOCKWISE] = False

    def set_motion_turns(self, motion: "Motion", new_turns: Turns) -> None:
        """Set the motion's turns and update related properties."""
        beat_index = self._calculate_beat_index()

        if new_turns == "fl":
            self.turns_widget.json_turns_updater.update_prefloat_values_in_json(
                motion, beat_index
            )

        self.turns_widget.json_turns_updater.update_turns_in_json(motion, new_turns)
