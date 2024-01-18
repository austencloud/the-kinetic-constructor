from typing import TYPE_CHECKING, Tuple
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph

from PyQt6.QtCore import Qt


class ArrowMovementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def handle_arrow_movement(self, key, shift_held) -> None:
        if not self.pictograph.selected_arrow:
            return

        adjustment_increment = 20 if shift_held else 5
        adjustment = self.get_adjustment(key, adjustment_increment)
        self.pictograph.arrow_placement_manager.special_placement_manager.update_arrow_adjustments_in_json(
            adjustment, self.pictograph.selected_arrow
        )
        self.pictograph.arrow_placement_manager.update_arrow_placement()

    def get_adjustment(self, key, increment) -> Tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment
