from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from Enums.Enums import Turns
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from .turns_widget import TurnsWidget


class TurnsAdjuster:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.graph_editor = self.turns_widget.turns_box.graph_editor
        self.beat_frame = self.graph_editor.sequence_widget.beat_frame
        self.main_widget = self.graph_editor.main_widget
        self.json_turns_updater = self.main_widget.json_manager.updater.turns_updater
        self.color = self.turns_widget.turns_box.color

    def adjust_turns(self, adjustment: Union[int, float]) -> None:
        """Adjust turns for the currently selected motion."""
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        turns = self.turns_widget.display_frame.turns_label.text()

        if turns == "fl" and adjustment < 0:
            QApplication.restoreOverrideCursor()
            return

        current_turns = self._convert_turns_to_num(turns)
        new_turns = self._calculate_new_turns(current_turns, adjustment)

        self.set_turns(new_turns)
        QApplication.restoreOverrideCursor()

    def set_turns(self, new_turns: Turns) -> None:
        """Set the new turns value."""
        matching_motion = (
            self.beat_frame.get.currently_selected_beat_view().beat.motions[self.color]
        )

        self.json_turns_updater.update_turns_in_json(matching_motion, new_turns)
        self.turns_widget.display_frame.update_turns_display(matching_motion, new_turns)
        self.main_widget.construct_tab.option_picker.updater.update_option_picker()
        validation_engine = self.main_widget.json_manager.ori_validation_engine
        validation_engine.run(True)

        self.beat_frame.updater.update_beats_from_current_sequence_json()
        self.beat_frame.sequence_widget.graph_editor.update_graph_editor()

    def _calculate_new_turns(
        self, current_turns: Turns, adjustment: Union[int, float]
    ) -> Turns:
        """Calculate the new turns value."""
        if current_turns == "fl" and adjustment > 0:
            return 0
        if current_turns == 0 and adjustment < 0:
            return "fl"
        return max(0, min(3, current_turns + adjustment))

    def _convert_turns_to_num(self, turns: Union[int, float, str]) -> Union[int, float]:
        """Convert turns from string to numerical representation."""
        if turns == "fl":
            return "fl"
        return int(turns) if turns in ["0", "1", "2", "3"] else float(turns)
