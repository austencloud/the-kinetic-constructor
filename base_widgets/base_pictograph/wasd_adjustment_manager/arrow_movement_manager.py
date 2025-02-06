from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


from PyQt6.QtCore import Qt


class ArrowMovementManager:
    def __init__(self, pictograph: "BasePictograph") -> None:
        self.pictograph = pictograph
        self.data_updater = (
            self.pictograph.arrow_placement_manager.special_positioner.data_updater
        )

    def handle_arrow_movement(
        self, pictograph: "BasePictograph", key, shift_held, ctrl_held
    ) -> None:
        self.graph_editor = pictograph.main_widget.sequence_widget.graph_editor
        selected_arrow = self.graph_editor.selection_manager.selected_arrow

        if not selected_arrow:
            return

        adjustment_increment = 5
        if shift_held:
            adjustment_increment = 20
        if shift_held and ctrl_held:
            adjustment_increment = 200

        adjustment = self.get_adjustment(key, adjustment_increment)

        self.data_updater.update_arrow_adjustments_in_json(adjustment, selected_arrow)
        self.data_updater.mirrored_entry_manager.update_mirrored_entry_in_json(
            selected_arrow
        )
        pictograph.arrow_placement_manager.update_arrow_placements()
        QApplication.processEvents()
        visible_pictographs = self.get_visible_pictographs()
        for pictograph in visible_pictographs:
            pictograph.arrow_placement_manager.update_arrow_placements()

    def get_visible_pictographs(self) -> list["BasePictograph"]:
        visible_pictographs = []
        for pictograph_list in self.pictograph.main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if pictograph.view:
                    if pictograph.view.isVisible():
                        visible_pictographs.append(pictograph)
        return visible_pictographs

    def get_adjustment(self, key, increment) -> tuple[int, int]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        return dx * increment, dy * increment
