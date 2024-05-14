import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager import SettingsManager
    from widgets.pictograph.pictograph import Pictograph


class GridVisibilityManager:
    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.non_radial_visible = self.load_visibility_settings()

    def load_visibility_settings(self) -> bool:
        return self.settings_manager.get_setting("non_radial_points_visibility", True)

    def save_visibility_settings(self):
        self.settings_manager.set_setting(
            "non_radial_points_visibility", self.non_radial_visible
        )
        self.settings_manager.save_settings()

    def toggle_visibility(self):
        self.non_radial_visible = not self.non_radial_visible
        self.save_visibility_settings()
        self.apply_visibility_to_all_pictographs()

    def apply_visibility_to_all_pictographs(self):
        for (
            pictograph_list
        ) in self.settings_manager.main_window.main_widget.pictograph_cache.values():
            for pictograph in pictograph_list.values():
                if hasattr(pictograph, "grid"):
                    pictograph.grid.toggle_non_radial_points_visibility(
                        self.non_radial_visible
                    )
