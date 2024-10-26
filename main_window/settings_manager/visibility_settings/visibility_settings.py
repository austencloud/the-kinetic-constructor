from typing import TYPE_CHECKING
from .glyph_visibility_manager import GlyphVisibilityManager
from .grid_visibility_manager import GridVisibilityManager

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:
    DEFAULT_VISIBILITY_SETTINGS = {
        "glyph_visibility": {
            "VTG": False,
            "TKA": True,
            "Elemental": False,
            "EndPosition": False,
            "Reversals": False,
        },
        "grid_visibility": {
            "non_radial_points": True,
        },
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance
        self.glyph_visibility_manager = GlyphVisibilityManager(self)
        self.grid_visibility_manager = GridVisibilityManager(self)

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        # Retrieve glyph visibility with default fallback
        return self.settings.value(
            f"visibility/glyph_visibility/{glyph_type}",
            self.DEFAULT_VISIBILITY_SETTINGS["glyph_visibility"].get(glyph_type, False),
            type=bool,
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        # Update the visibility setting for a specific glyph
        self.settings.setValue(f"visibility/glyph_visibility/{glyph_type}", visible)
        self.glyph_visibility_manager.apply_glyph_visibility()

    def get_grid_visibility(self, element: str) -> bool:
        # Retrieve grid visibility with default fallback
        return self.settings.value(
            f"visibility/grid_visibility/{element}",
            self.DEFAULT_VISIBILITY_SETTINGS["grid_visibility"].get(element, True),
            type=bool,
        )

    def set_grid_visibility(self, element: str, visible: bool) -> None:
        # Update the visibility setting for a specific grid element
        self.settings.setValue(f"visibility/grid_visibility/{element}", visible)
        self.grid_visibility_manager.apply_visibility_to_all_pictographs()
