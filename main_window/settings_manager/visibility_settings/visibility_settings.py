import json
from typing import TYPE_CHECKING

from main_window.settings_manager.visibility_settings.glyph_visibility_manager import GlyphVisibilityManager
from main_window.settings_manager.visibility_settings.grid_visibility_manager import GridVisibilityManager


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    DEFAULT_VISIBILITY_SETTINGS = {
        "glyph_visibility": {
            "VTG": False,
            "TKA": True,
            "Elemental": False,
            "EndPosition": False,
        },
        "grid_visibility": {
            "non_radial_points": True,
        },
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "visibility", self.DEFAULT_VISIBILITY_SETTINGS
        )
        self.glyph_visibility_manager = GlyphVisibilityManager(self)
        self.grid_visibility_manager = GridVisibilityManager(self)

    def get_glyph_visibility(self):
        return self.settings.get(
            "glyph_visibility", self.DEFAULT_VISIBILITY_SETTINGS["glyph_visibility"]
        )

    def get_grid_visibility(self):
        return self.settings.get(
            "grid_visibility", self.DEFAULT_VISIBILITY_SETTINGS["grid_visibility"]
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        self.settings["glyph_visibility"][glyph_type] = visible
        self.update_visibility_settings_in_json()

    def set_grid_visibility(self, grid_element: str, visible: bool) -> None:
        self.settings["grid_visibility"][grid_element] = visible
        self.update_visibility_settings_in_json()

    def update_visibility_settings_in_json(self):
        # get the json file and properly update just the part of the settings file that has visibility settings
        json_file = self.settings_manager.settings_json
        with open(json_file, "r") as file:
            settings = json.load(file)
        settings["visibility"] = self.settings
        with open(json_file, "w") as file:
            json.dump(settings, file, indent=4)
