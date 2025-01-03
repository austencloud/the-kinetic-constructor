from PyQt6.QtWidgets import QWidget, QGraphicsItemGroup, QCheckBox, QHBoxLayout
from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.pictograph_view import PictographView
from base_widgets.base_pictograph.tka_glyph.base_glyph import BaseGlyph
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from main_window.main_widget.settings_dialog.visibility_tab import VisibilityTab


class VisibilityTabPictographView(PictographView):
    def __init__(self, pictograph: "BasePictograph", visibility_tab: "VisibilityTab"):
        super().__init__(pictograph)
        self.visibility_tab = visibility_tab
        self.set_clickable_glyphs()

    def set_clickable_glyphs(self):
        """Enable glyphs to be clickable and update visibility settings."""
        glyphs: list[Union[BaseGlyph, QGraphicsItemGroup, QGraphicsSvgItem]] = [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
        ]
        for glyph in glyphs:
            glyph.mousePressEvent = self._create_mouse_press_event(glyph)

    def _create_mouse_press_event(self, glyph):
        def mousePressEvent(event):
            self._toggle_glyph_visibility(glyph)

        return mousePressEvent

    def _toggle_glyph_visibility(self, glyph: BaseGlyph):
        """Toggle visibility for a glyph and update the checkbox."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        manager = settings.glyph_visibility_manager

        current_visibility = manager.should_glyph_be_visible(glyph.name)
        settings.set_glyph_visibility(glyph.name, not current_visibility)
        self.visibility_tab.update_checkboxes()
