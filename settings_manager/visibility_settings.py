from typing import TYPE_CHECKING

from widgets.menu_bar.glyph_visibility_manager import GlyphVisibilityManager
from widgets.menu_bar.grid_visibility_manager import GridVisibilityManager


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
            "visibility_settings", self.DEFAULT_VISIBILITY_SETTINGS
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

        