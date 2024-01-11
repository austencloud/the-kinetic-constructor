from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class TurnAdjustmentManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def handle_half_turns(self, key) -> None:
        if not self.pictograph.selected_arrow:
            return

        half_turn_adjustment = -0.5 if key == Qt.Key.Key_Q else 0.5
        self.adjust_turns(half_turn_adjustment)

    def adjust_turns(self, adjustment: float) -> None:
        selected_motion = self.pictograph.selected_arrow.motion
        new_turns = max(0, min(3, selected_motion.turns + adjustment))
        new_turns = int(new_turns) if new_turns.is_integer() else new_turns
        self.pictograph.update_pictograph(
            {f"{self.pictograph.selected_arrow.color}_turns": new_turns}
        )
