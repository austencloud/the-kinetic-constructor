from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
from Enums.Enums import Turns
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

        self.turns_adjusted.connect(
            self.beat_frame.updater.update_beats_from_current_sequence_json
        )

    def adjust_turns(self, adjustment: Union[int, float]) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        current_turns = self.get_current_turns_value()
        self.pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        matching_motion = self.pictograph.motions[self.color]
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

        motion = self.pictograph.motions[self.color]
        self.turns_widget.turns_updater._adjust_turns_for_pictograph(
            self.pictograph, adjustment
        )
        self.turns_widget.update_turns_display(matching_motion, new_turns)
        self._repaint_views()
        need_to_determine_new_letter: bool = self.determine_if_new_letter_is_necessary(
            motion, new_turns
        )
        if need_to_determine_new_letter:
            new_letter = self.main_widget.letter_determiner.determine_letter(motion)
        else:
            new_letter = None
        self.turns_widget.turns_box.prop_rot_dir_button_manager._update_pictograph_and_json(
            motion, new_letter
        )
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.main_widget.build_tab.manual_builder.option_picker.update_option_picker()
        self.turns_adjusted.emit(new_turns)
        QApplication.restoreOverrideCursor()

    def determine_if_new_letter_is_necessary(self, motion: Motion, new_turns) -> bool:
        if new_turns == "fl":
            return True
        if motion.turns == "fl" and new_turns >= 0:
            return True

    def _repaint_views(self):
        """Repaint the pictograph and GE pictograph views to reflect the change."""
        self.pictograph.view.repaint()
        GE_pictograph = (
            self.turns_widget.turns_box.adjustment_panel.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        GE_pictograph.view.repaint()
        # GE_pictograph.updater.update_pictograph()
        QApplication.processEvents()

    def direct_set_turns(self, new_turns: Turns) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.pictograph = (
            self.graph_editor.pictograph_container.GE_pictograph_view.get_current_pictograph()
        )
        self._update_motion_properties(new_turns)
        pictograph_index = self.beat_frame.get.index_of_currently_selected_beat()
        self.json_manager.updater.turns_updater.update_turns_in_json_at_index(
            pictograph_index + 2, self.color, new_turns
        )
        self.pictograph.motions[self.color].turns = new_turns
        self.turns_widget.update_turns_display(
            self.pictograph.motions[self.color], new_turns
        )
        self.json_validation_engine.run(is_current_sequence=True)
        self.main_widget.build_tab.manual_builder.option_picker.update_option_picker()
        self.turns_adjusted.emit(new_turns)
        QApplication.restoreOverrideCursor()

    def get_current_turns_value(self) -> Turns:
        return self._get_turns()

    def _get_turns(self) -> Turns:
        turns = self.turns_widget.turns_display_frame.turns_label.text()
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
        self.turns_widget.update_turns_display(turns)

    def _update_motion_properties(self, new_turns) -> None:
        for motion in self.pictograph.motions.values():
            if motion.color == self.turns_widget.turns_box.color:
                self.turns_widget.turns_updater.set_motion_turns(motion, new_turns)
