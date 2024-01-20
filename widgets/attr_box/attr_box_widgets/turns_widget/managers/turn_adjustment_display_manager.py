from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import (
    Turns,
)

if TYPE_CHECKING:
    from widgets.attr_box.attr_box_widgets.turns_widget.turns_widget import TurnsWidget
    from widgets.attr_box.attr_box import AttrBox



class TurnsAdjustmentDisplayManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.attr_box = turns_widget.attr_box
        self.turns_widget = turns_widget

    def adjust_turns(self, adjustment: Turns) -> None:
        """Adjust turns for a given pictograph based on the attribute type."""
        turns = self.turns_widget.turns_display_manager.turns_display.text()
        turns = self.turns_widget._convert_turns_from_str_to_num(turns)
        turns = self.turns_widget.updater._clamp_turns(turns + adjustment)
        turns = self.convert_turn_floats_to_ints(turns)
        self.turns_widget.turns_display_manager.update_turns_display(str(turns))

        for (
            pictograph
        ) in self.attr_box.attr_panel.filter_tab.scroll_area.pictographs.values():
            if (
                pictograph.letter_type
                == self.attr_box.attr_panel.filter_tab.letter_type
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
        for (
            pictograph
        ) in self.attr_box.attr_panel.filter_tab.scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                if self.turns_widget.turn_adjust_manager.is_motion_relevant(motion):
                    self.turns_widget.updater.update_motion_properties(
                        motion, new_turns
                    )
