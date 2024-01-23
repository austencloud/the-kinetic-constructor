from typing import TYPE_CHECKING
from Enums import LetterType
from constants import DASH, STATIC
from utilities.TypeChecking.TypeChecking import (
    Turns,
)

if TYPE_CHECKING:
    from widgets.turns_box.turns_box_widgets.turns_widget.turns_widget import (
        TurnsWidget,
    )


class TurnsAdjustmentDisplayManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_box = turns_widget.turns_box
        self.turns_widget = turns_widget
        self.pictographs = (
            self.turns_box.turns_panel.filter_tab.section.scroll_area.pictographs.values()
        )

    def adjust_turns(self, adjustment: Turns) -> None:
        """Adjust turns for a given pictograph based on the attribute type."""
        turns = self.turns_widget.turns_display_manager.turns_display.text()
        turns = self.turns_widget._convert_turns_from_str_to_num(turns)
        turns = self.turns_widget.updater._clamp_turns(turns + adjustment)
        turns = self.convert_turn_floats_to_ints(turns)
        self.turns_widget.turns_display_manager.update_turns_display(str(turns))
        letter_type = self.turns_box.turns_panel.filter_tab.section.letter_type
        if self.turns_box.attribute_value in [STATIC, DASH]:
            button_manager = (
                self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager
            )
            button_manager.update_visibility_based_on_motion(letter_type, turns)
        for pictograph in self.pictographs:
            if (
                LetterType.get_letter_type(pictograph.letter)
                == self.turns_box.turns_panel.filter_tab.section.letter_type
            ):
                self.turns_widget.updater._adjust_turns_for_pictograph(
                    pictograph, adjustment
                )

    def convert_turn_floats_to_ints(self, turns: Turns) -> Turns:
        if turns in [0.0, 1.0, 2.0, 3.0]:
            return int(turns)
        else:
            return turns

    def set_turns(self, new_turns: Turns) -> None:
        self.turns_widget.turns_display_manager.update_turns_display(new_turns)
        for pictograph in self.pictographs:
            for motion in pictograph.motions.values():
                if self.turns_widget.turn_adjust_manager.is_motion_relevant(motion):
                    self.turns_widget.updater.update_motion_properties(
                        motion, new_turns
                    )
        turns = self.turns_widget.turns_display_manager.turns_display.text()
        turns = self.turns_widget._convert_turns_from_str_to_num(turns)
        turns = self.convert_turn_floats_to_ints(turns)
        letter_type = self.turns_box.turns_panel.filter_tab.section.letter_type
        if self.turns_box.attribute_value in [STATIC, DASH]:
            button_manager = (
                self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager
            )
            button_manager.update_visibility_based_on_motion(letter_type, turns)
            
    def reset_turns_display(self) -> None:
        self.turns_widget.turns_display_manager.update_turns_display("0")
        for pictograph in self.pictographs:
            for motion in pictograph.motions.values():
                if self.turns_widget.turn_adjust_manager.is_motion_relevant(motion):
                    self.turns_widget.updater.update_motion_properties(motion, 0)

    def get_current_turns_value(self) -> Turns:
        return self.turns_widget.turns_display_manager.turns_display.text()
