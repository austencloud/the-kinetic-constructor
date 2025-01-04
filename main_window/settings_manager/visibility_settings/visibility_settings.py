from typing import TYPE_CHECKING

from base_widgets.base_pictograph.glyphs.glyph_toggler import (
    GlyphToggler,
)
from base_widgets.base_pictograph.grid.non_radial_points_toggler import (
    NonRadialPointsToggler,
)

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class VisibilitySettings:

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings
        self.glyph_visibility_manager = GlyphToggler(self)

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        return self.settings.value(
            f"visibility/glyph_visibility/{glyph_type}",
            False,
            type=bool,
        )

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        self.settings.setValue(f"visibility/glyph_visibility/{glyph_type}", visible)
        self.glyph_visibility_manager.apply_glyph_visibility()

    def get_non_radial_visibility(self, element: str) -> bool:
        return self.settings.value(
            f"visibility/grid_visibility/{element}", True, type=bool
        )

    def set_non_radial_visibility(self, visible: bool):
        self.non_radial_visible = visible
        self.settings.setValue(f"visibility/grid_visibility/non_radial_points", visible)
