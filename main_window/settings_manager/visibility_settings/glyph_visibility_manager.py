from typing import TYPE_CHECKING
from Enums.letters import Letter
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )


class GlyphVisibilityManager:
    def __init__(self, visibility_settings: "VisibilitySettings") -> None:
        self.visibility_settings = visibility_settings
        self.main_window = visibility_settings.settings_manager.main_window

    def apply_visibility(self, glyph_type: str, pictograph: "BasePictograph"):
        visibility = self.visibility_settings.get_glyph_visibility(glyph_type)
        if glyph_type == "VTG":
            pictograph.vtg_glyph.setVisible(visibility)
        elif glyph_type == "TKA":
            pictograph.tka_glyph.setVisible(visibility)
        elif glyph_type == "Elemental":
            pictograph.elemental_glyph.setVisible(visibility)
        elif glyph_type == "Positions":
            pictograph.start_to_end_pos_glyph.setVisible(visibility)
        elif glyph_type == "Reversals":
            if pictograph.blue_reversal:
                pictograph.blue_reversal_symbol.setVisible(visibility)
            if pictograph.red_reversal:
                pictograph.red_reversal_symbol.setVisible(visibility)

    def apply_current_visibility_settings(self, pictograph: "BasePictograph"):
        for glyph_type in ["VTG", "TKA", "Elemental", "Positions", "Reversals"]:
            self.apply_visibility(glyph_type, pictograph)

        if pictograph.letter in [Letter.α, Letter.β, Letter.Γ]:
            pictograph.start_to_end_pos_glyph.setVisible(False)

    def apply_glyph_visibility(self):
        # Apply current settings to all visible pictographs
        beat_views = self.main_window.main_widget.sequence_widget.beat_frame.beats
        beats = [beat_view.beat for beat_view in beat_views]
        for pictograph_key_with_scene in list(
            self.main_window.main_widget.pictograph_cache.values()
        ):
            for scene in pictograph_key_with_scene.values():
                if scene.view:
                    if scene.view.isVisible():
                        self.apply_current_visibility_settings(scene)
        for beat in beats:
            if beat:
                self.apply_current_visibility_settings(beat)
        for (
            option
        ) in self.main_window.main_widget.construct_tab.option_picker.option_pool:
            if option:
                self.apply_current_visibility_settings(option)
        # self.apply_current_visibility_settings(
        #     self.main_window.main_widget.settings_dialog.visibility_tab.pictograph_view.pictograph
        # )

    def should_glyph_be_visible(self, glyph_type: str) -> bool:
        """Check if a glyph type should be visible based on current settings."""
        return self.visibility_settings.get_glyph_visibility(glyph_type)

    def toggle_glyph_visibility(self, name: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_settings.set_glyph_visibility(name, is_checked)
