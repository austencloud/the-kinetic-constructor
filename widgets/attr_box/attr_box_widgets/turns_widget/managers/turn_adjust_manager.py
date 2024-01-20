from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import (
    Turns,
)

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox
    from objects.motion.motion import Motion
    from ..turns_widget import TurnsWidget


class TurnAdjustManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.attr_box: "AttrBox" = turns_widget.attr_box
        self.turns_widget = turns_widget


    def setup_adjust_turns_buttons(self) -> None:
        self.turns_widget.button_manager.setup_adjust_turns_buttons()

    def is_motion_relevant(self, motion: "Motion") -> bool:
        return self.turns_widget.relevance_checker.is_motion_relevant(motion)

    def adjust_turns(self, adjustment: Turns) -> None:
        self.turns_widget.display_manager.adjust_turns(adjustment)

    def unpress_vtg_buttons(self) -> None:
        """Unpress the vtg buttons."""
        if hasattr(self.attr_box, "same_button"):
            self.attr_box.rot_dir_button_manager.same_button.unpress()
            self.attr_box.rot_dir_button_manager.opp_button.unpress()

    def update_motion_properties(self, motion: "Motion", new_turns: Turns) -> None:
        self.turns_widget.updater.update_motion_properties(motion, new_turns)





