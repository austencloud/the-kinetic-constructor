from PyQt6.QtWidgets import QGraphicsItemGroup
from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph
from objects.grid import NonRadialGridPoints, NonRadialPoint
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab_pictograph import (
        VisibilityTabPictograph,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class GridManager:
    """Manages non-radial grid points hover and click interactions."""

    def __init__(self, pictograph: "VisibilityTabPictograph"):
        self.pictograph = pictograph

        self.non_radial_points = self._collect_non_radial_points()
        self.initialize_interactions()

    def _collect_non_radial_points(self) -> NonRadialGridPoints:
        """Retrieve the non-radial points group from the grid."""
        return self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial"
        )

    def initialize_interactions(self):
        """Attach hover and click events to non-radial points."""
        for point in self.non_radial_points.child_points:
            point.mousePressEvent = self._create_click_event(point)
            point.hoverEnterEvent = self._create_hover_event(point, entering=True)
            point.hoverLeaveEvent = self._create_hover_event(point, entering=False)
            # point.setCursor(Qt.CursorShape.PointingHandCursor)

    def _create_hover_event(self, point: "NonRadialPoint", entering: bool):
        """Create a hover event for entering or leaving."""
        self.settings = self.pictograph.main_widget.settings_manager.visibility

        def hoverEvent(event):
            point.setCursor(Qt.CursorShape.PointingHandCursor)
            point.setOpacity(
                0.5
                if entering
                else (
                    1
                    if self.settings.get_grid_visibility(self.non_radial_points.name)
                    else 0.1
                )
            )

        return hoverEvent

    def _create_click_event(self, point: "NonRadialPoint"):
        """Create a click event for toggling non-radial points visibility."""

        def clickEvent(event):
            current_visibility = self.pictograph.view.settings.grid.non_radial_visible
            self.pictograph.view.settings.grid.set_non_radial_visibility(
                not current_visibility
            )
            self.non_radial_points.setOpacity(1 if not current_visibility else 0.1)
            self.pictograph.view.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent
