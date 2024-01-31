from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from Enums import LetterType


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

        self.pictograph.arrow_placement_manager.special_positioner.data_updater.mirrored_entry_handler.update_mirrored_entry_in_json(
            self.pictograph.selected_arrow
        )
        for pictograph in self.pictograph.scroll_area.sections_manager.get_section(
            LetterType.get_letter_type(self.pictograph.letter)
        ).pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()

    def get_adjustment(self, key, increment) -> tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment
