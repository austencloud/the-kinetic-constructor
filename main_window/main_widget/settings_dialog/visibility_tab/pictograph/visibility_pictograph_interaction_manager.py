from typing import Union, TYPE_CHECKING
from PyQt6.QtCore import Qt
from base_widgets.base_pictograph.glyphs.reversals_glyph import BeatReversalGlyph
from base_widgets.base_pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from base_widgets.base_pictograph.grid.grid import NonRadialPointsGroup
from Enums.Enums import Glyph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.pictograph.visibility_pictograph_view import (
        VisibilityPictographView,
    )


class VisibilityPictographInteractionManager:
    """Manages glyph and non-radial point interactions for the pictograph view."""

    def __init__(self, parent: "VisibilityPictographView"):
        self.parent = parent
        self.pictograph = parent.pictograph
        self.visibility_settings = parent.visibility_settings
        self.glyphs = parent.glyphs
        self.non_radial_points = parent.non_radial_points
        self._initialize_interactions()

    def _initialize_interactions(self):
        """Initialize all hover and click events for glyphs and non-radial points."""
        for glyph in self.glyphs:
            self._assign_glyph_events(glyph)
        self._assign_non_radial_point_events()

    def _assign_glyph_events(self, glyph: Glyph):
        """Assign hover and click events to a glyph."""
        glyph.mousePressEvent = self._create_click_event(glyph)
        glyph.setAcceptHoverEvents(True)
        glyph.hoverEnterEvent = self._create_hover_event(glyph, entering=True)
        glyph.hoverLeaveEvent = self._create_hover_event(glyph, entering=False)

        if isinstance(glyph, (StartToEndPosGlyph, BeatReversalGlyph)):
            for child in glyph.childItems():
                child.setCursor(Qt.CursorShape.PointingHandCursor)
                child.setAcceptHoverEvents(True)
                child.mousePressEvent = self._create_click_event(glyph)
                child.hoverEnterEvent = self._create_hover_event(child, entering=True)
                child.hoverLeaveEvent = self._create_hover_event(child, entering=False)

    def _assign_non_radial_point_events(self):
        """Assign hover and click events to non-radial points."""
        self.non_radial_points.setAcceptHoverEvents(True)
        self.non_radial_points.mousePressEvent = self._create_non_radial_click_event()
        self.non_radial_points.hoverEnterEvent = self._create_hover_event(
            self.non_radial_points, entering=True
        )
        self.non_radial_points.hoverLeaveEvent = self._create_hover_event(
            self.non_radial_points, entering=False
        )

    def _create_hover_event(
        self, item: Union[Glyph, NonRadialPointsGroup], entering: bool
    ):
        """Create a hover event for entering or leaving."""

        def hoverEvent(event):
            if entering:
                item.setOpacity(0.5)
                item.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.update_opacity(item)

        return hoverEvent

    def _create_click_event(self, glyph: Glyph):
        """Create a click event for toggling glyph visibility."""

        def clickEvent(event):
            current_visibility = self.visibility_settings.get_glyph_visibility(
                glyph.name
            )
            self.visibility_settings.set_glyph_visibility(
                glyph.name, not current_visibility
            )
            self.update_opacity(glyph)
            self.parent.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent

    def _create_non_radial_click_event(self):
        """Create a click event for toggling non-radial points visibility."""

        def clickEvent(event):
            current_visibility = self.visibility_settings.get_non_radial_visibility()
            self.visibility_settings.set_non_radial_visibility(not current_visibility)
            self.update_opacity(self.non_radial_points)
            self.parent.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent

    def update_opacity(self, item: Union[Glyph, NonRadialPointsGroup]):
        """Update the opacity of a glyph or non-radial point based on visibility settings."""
        if isinstance(item, NonRadialPointsGroup):
            visible = self.visibility_settings.get_non_radial_visibility()
        else:
            visible = self.visibility_settings.get_glyph_visibility(item.name)
        item.setOpacity(1 if visible else 0.1)
