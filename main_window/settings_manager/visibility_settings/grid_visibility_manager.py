from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from .visibility_settings import VisibilitySettings


class GridVisibilityManager:
    def __init__(self, visibility_settings: "VisibilitySettings") -> None:
        self.settings = visibility_settings
        self.settings_manager = visibility_settings.settings_manager
        self.non_radial_visible = self.settings.get_grid_visibility("non_radial_points")
        self.main_window = visibility_settings.settings_manager.main_window

    def save_non_radial_visibility(self, visible: bool):
        self.settings.set_grid_visibility("non_radial_points", visible)
        self.apply_grid_visibility()

    def set_non_radial_visibility(self, visible: bool):
        self.non_radial_visible = visible
        self.save_non_radial_visibility(visible)

    def apply_grid_visibility(self):
        self.non_radial_visible = self.settings.get_grid_visibility("non_radial_points")

        pictographs = (
            self.main_window.main_widget.pictograph_collector.collect_all_pictographs()
        )
        for pictograph in pictographs:
            pictograph.grid.toggle_non_radial_points_visibility(self.non_radial_visible)

    def toggle_grid_visibility(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.set_non_radial_visibility(is_checked)
        self.settings.set_grid_visibility("non_radial_points", is_checked)
