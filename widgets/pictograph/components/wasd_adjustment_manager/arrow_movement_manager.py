from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from Enums import LetterType
from constants import Type1

from utilities.TypeChecking.letter_lists import Type1_non_hybrid_letters

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph

from PyQt6.QtCore import Qt


class ArrowMovementManager:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph

    def handle_arrow_movement(self, key, shift_held, ctrl_held) -> None:
        if not self.pictograph.selected_arrow:
            return

        if shift_held and ctrl_held:
            adjustment_increment = 200
        elif shift_held:
            adjustment_increment = 20
        else:
            adjustment_increment = 5
        adjustment = self.get_adjustment(key, adjustment_increment)

        self.pictograph.arrow_placement_manager.special_positioner.data_updater.update_arrow_adjustments_in_json(
            adjustment, self.pictograph.selected_arrow
        )

        if LetterType.get_letter_type(self.pictograph.letter) == Type1 and self.pictograph.letter in Type1_non_hybrid_letters:
            self.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_handler.update_mirrored_entry_in_json(
                adjustment, self.pictograph.selected_arrow
            )

        self.pictograph.arrow_placement_manager.update_arrow_positions()


    def get_adjustment(self, key, increment) -> tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment
