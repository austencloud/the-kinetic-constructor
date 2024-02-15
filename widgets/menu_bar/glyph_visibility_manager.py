from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main import MainWindow
    from widgets.pictograph.pictograph import Pictograph


class GlyphVisibilityToggler:
    def __init__(self, main_window: "MainWindow"):
        self.main_window = main_window
        self.visibility_states: dict[str, bool] = {}
        # self.init_states()

    def init_states(self):
        settings_manager = self.main_window.settings_manager
        for glyph_type in ["VTG", "TKA", "Elemental"]:
            self.visibility_states[glyph_type] = settings_manager.get_glyph_visibility(
                glyph_type
            )

    def toggle_visibility(self, glyph_type):
        if glyph_type in self.visibility_states:
            self.visibility_states[glyph_type] = not self.visibility_states[glyph_type]
            self.apply_visibility(glyph_type)

    def apply_visibility(self, glyph_type, pictograph: "Pictograph"):
        if glyph_type == "VTG":
            pictograph.vtg_glyph.setVisible(self.visibility_states[glyph_type])
        elif glyph_type == "TKA":
            pictograph.tka_glyph.setVisible(self.visibility_states[glyph_type])
        elif glyph_type == "Elemental":
            pictograph.elemental_glyph.setVisible(self.visibility_states[glyph_type])

    def apply_current_visibility_settings(self, pictograph: "Pictograph"):
        settings_manager = self.main_window.settings_manager
        for glyph_type in ["VTG", "TKA", "Elemental"]:
            visibility = settings_manager.get_glyph_visibility(glyph_type)
            self.visibility_states[glyph_type] = visibility
            self.apply_visibility(glyph_type, pictograph)

    def should_glyph_be_visible(self, glyph_type: str) -> bool:
        settings_manager = self.main_window.settings_manager
        return settings_manager.get_glyph_visibility(glyph_type)
