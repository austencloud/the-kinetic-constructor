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

    def _collect_non_radial_points(self) -> NonRadialGridPoints:
        """Retrieve the non-radial points group from the grid."""
        return self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial"
        )

    def initialize_interactions(self):
        """Attach hover and click events to non-radial points."""
        if not self.non_radial_points:
            print("No non-radial points found")
            return

        for point in self.non_radial_points.child_points:
            print(f"Assigning events to point: {point.point_id}")
            point.setAcceptHoverEvents(True)  # Explicitly accept hover events
            point.setAcceptedMouseButtons(Qt.MouseButton.LeftButton)  # Accept mouse buttons
            point.mousePressEvent = self._create_click_event(point)
            point.hoverEnterEvent = self._create_hover_event(point, entering=True)
            point.hoverLeaveEvent = self._create_hover_event(point, entering=False)

        print("Non-radial points interaction initialized.")


    def _create_hover_event(self, point: "NonRadialPoint", entering: bool):
        """Create a hover event for entering or leaving."""

        def hoverEvent(event):
            point.setCursor(Qt.CursorShape.PointingHandCursor)
            point.setOpacity(
                0.5
                if entering
                else (
                    1
                    if self.pictograph.main_widget.settings_manager.visibility.grid.non_radial_visible
                    else 0.1
                )
            )

        return hoverEvent

    def _create_click_event(self, point: "NonRadialPoint"):
        """Create a click event for toggling non-radial points visibility."""

        def clickEvent(event):
            current_visibility = (
                self.pictograph.main_widget.settings_manager.visibility.grid.non_radial_visible
            )
            self.pictograph.main_widget.settings_manager.visibility.grid.set_non_radial_visibility(
                not current_visibility
            )
            point.setOpacity(1 if not current_visibility else 0.1)
            self.pictograph.main_widget.settings_dialog.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent
