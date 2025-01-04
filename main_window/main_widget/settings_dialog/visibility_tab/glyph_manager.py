from PyQt6.QtWidgets import QGraphicsItemGroup
from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.glyphs.reversals_glyph import BeatReversalGlyph
from base_widgets.base_pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab_pictograph import (
        VisibilityTabPictograph,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union[
    "BeatReversalGlyph", "BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"
]


class GlyphManager:
    """Handles glyph hover and click interactions."""

    def __init__(self, pictograph: "VisibilityTabPictograph"):
        self.pictograph = pictograph
        self.glyphs = self._collect_glyphs()
        self.initialize_glyph_interactions()

    def _collect_glyphs(self) -> list[Glyph]:
        """Collect all glyphs for interaction."""
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def initialize_glyph_interactions(self):
        """Attach hover and click events to glyphs."""
        for glyph in self.glyphs:
            glyph.mousePressEvent = self._create_click_event(glyph)
            glyph.setAcceptHoverEvents(True)
            glyph.hoverEnterEvent = self._create_hover_event(glyph, entering=True)
            glyph.hoverLeaveEvent = self._create_hover_event(glyph, entering=False)
            glyph.setCursor(Qt.CursorShape.PointingHandCursor)
            if glyph.__class__ == StartToEndPosGlyph:
                for child in glyph.childItems():
                    child.setCursor(Qt.CursorShape.PointingHandCursor)
                    child.mousePressEvent = self._create_click_event(glyph)
                    child.setAcceptHoverEvents(True)
                    child.hoverEnterEvent = self._create_hover_event(
                        child, entering=True
                    )
                    child.hoverLeaveEvent = self._create_hover_event(
                        child, entering=False
                    )
            elif glyph.__class__ == BeatReversalGlyph:
                for child in glyph.reversal_items.values():
                    child.setCursor(Qt.CursorShape.PointingHandCursor)
                    child.mousePressEvent = self._create_click_event(glyph)
                    child.setAcceptHoverEvents(True)
                    child.hoverEnterEvent = self._create_hover_event(
                        child, entering=True
                    )
                    child.hoverLeaveEvent = self._create_hover_event(
                        child, entering=False
                    )

    def _create_hover_event(self, glyph: Glyph, entering: bool):
        """Create a hover event for entering or leaving."""

        def hoverEvent(event):
            glyph.setOpacity(
                0.5
                if entering
                else (
                    1
                    if self.pictograph.view.visibility_settings.get_glyph_visibility(
                        glyph.name
                    )
                    else 0.1
                )
            )
            for child in glyph.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)

        return hoverEvent

    def _create_click_event(self, glyph: Glyph):
        """Create a click event for toggling glyph visibility."""

        def clickEvent(event):
            current_visibility = (
                self.pictograph.view.visibility_settings.get_glyph_visibility(
                    glyph.name
                )
            )
            self.pictograph.view.visibility_settings.set_glyph_visibility(
                glyph.name, not current_visibility
            )
            glyph.setOpacity(1 if not current_visibility else 0.1)
            self.pictograph.view.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent
