from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from base_widgets.base_pictograph.grid.grid import Grid
    from ....main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )


class NonRadialPointsToggler:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.settings_manager = self.settings.settings_manager
        self.non_radial_visible = self.settings.get_non_radial_visibility(
            "non_radial_points"
        )

    def toggle_non_radial_points(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.settings.set_non_radial_visibility(is_checked)
        self.non_radial_visible = self.settings.get_non_radial_visibility(
            "non_radial_points"
        )

        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        for pictograph in pictographs:
            pictograph.grid.toggle_non_radial_points_visibility(self.non_radial_visible)
