from typing import TYPE_CHECKING, Union
from Enums.letters import Letter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsTextItem
from base_widgets.base_pictograph.glyphs.elemental_glyph.elemental_glyph import (
    ElementalGlyph,
)
from base_widgets.base_pictograph.glyphs.reversals_glyph import BeatReversalGlyph
from base_widgets.base_pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from base_widgets.base_pictograph.glyphs.tka_glyph.tka_glyph import TKA_Glyph
from base_widgets.base_pictograph.glyphs.vtg_glyph.vtg_glyph import VTG_Glyph

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.settings_manager.visibility_settings.visibility_settings import (
        VisibilitySettings,
    )
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union[
    QGraphicsTextItem,
    QGraphicsSvgItem,
    BeatReversalGlyph,
    ElementalGlyph,
    StartToEndPosGlyph,
    TKA_Glyph,
    VTG_Glyph,
]

class GlyphVisibilityManager:
    def __init__(self, visibility_settings: "VisibilitySettings") -> None:
        self.visibility_settings = visibility_settings
        self.main_window = visibility_settings.settings_manager.main_window

    def apply_visibility(self, glyph_type: str, pictograph: "BasePictograph"):
        visibility = self.visibility_settings.get_glyph_visibility(glyph_type)
        glyph_mapping: dict[str, list[Glyph]] = {
            "VTG": [pictograph.vtg_glyph],
            "TKA": [pictograph.tka_glyph],
            "Elemental": [pictograph.elemental_glyph],
            "Positions": [pictograph.start_to_end_pos_glyph],
            "Reversals": [
                pictograph.blue_reversal_symbol if pictograph.blue_reversal else None,
                pictograph.red_reversal_symbol if pictograph.red_reversal else None,
            ],
        }

        glyphs = glyph_mapping.get(glyph_type, [])
        for glyph in glyphs:
            if glyph:
                glyph.setVisible(visibility)

    def apply_current_visibility_settings(self, pictograph: "BasePictograph"):
        for glyph_type in ["VTG", "TKA", "Elemental", "Positions", "Reversals"]:
            self.apply_visibility(glyph_type, pictograph)

        if pictograph.letter in [Letter.α, Letter.β, Letter.Γ]:
            pictograph.start_to_end_pos_glyph.setVisible(False)

    def apply_glyph_visibility(self):
        pictographs = (
            self.main_window.main_widget.pictograph_collector.collect_all_pictographs()
        )
        for pictograph in pictographs:
            self.apply_current_visibility_settings(pictograph)

    def should_glyph_be_visible(self, glyph_type: str) -> bool:
        """Check if a glyph type should be visible based on current settings."""
        return self.visibility_settings.get_glyph_visibility(glyph_type)

    def toggle_glyph_visibility(self, name: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_settings.set_glyph_visibility(name, is_checked)
