from PyQt6.QtWidgets import QGraphicsItemGroup
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from base_widgets.base_pictograph.glyphs.reversals_glyph import BeatReversalGlyph
from base_widgets.base_pictograph.glyphs.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from base_widgets.base_pictograph.pictograph_view import PictographView
from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import Qt, QEvent
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph
from objects.grid import NonRadialGridPoints

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem", "BeatReversalGlyph"]


class VisibilityTabPictographView(PictographView):
    """Manages interactions with pictograph view, including hover and click behavior."""

    def __init__(self, visibility_tab: "VisibilityTab", pictograph: BasePictograph):
        self.pictograph = pictograph
        self.visibility_tab = visibility_tab
        self.settings = visibility_tab.settings
        self.main_widget = visibility_tab.main_widget
        self.pictograph = self._initialize_example_pictograph()
        super().__init__(pictograph)
        self.glyphs = self._collect_glyphs()
        self.non_radial_points = self._collect_non_radial_points()
        self._apply_initial_visibility()
        self._initialize_interactions()

    def _initialize_example_pictograph(self) -> BasePictograph:
        """Create and initialize the example pictograph."""
        example_data = {
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "blue_motion_type": "pro",
            "red_motion_type": "pro",
        }
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            example_data
        )
        self.pictograph.red_reversal = True
        self.pictograph.blue_reversal = True
        self.pictograph.updater.update_pictograph(pictograph_dict)

        glyphs: list[Glyph] = [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]
        for glyph in glyphs:
            glyph.setVisible(True)
        self.pictograph.grid.toggle_non_radial_points_visibility(True)

        return self.pictograph

    def _collect_glyphs(self) -> list[Glyph]:
        """Collect all glyphs for interaction."""
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def _collect_non_radial_points(self) -> QGraphicsItemGroup:
        """Retrieve the non-radial points group from the grid."""
        return self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial"
        )

    def _apply_initial_visibility(self):
        """Set initial visibility for glyphs and non-radial points."""
        for glyph in self.glyphs:
            glyph.setOpacity(
                1 if self.settings.glyph.should_glyph_be_visible(glyph.name) else 0.1
            )
        self.non_radial_points.setOpacity(
            1 if self.settings.grid.non_radial_visible else 0.1
        )

    def _initialize_interactions(self):
        """Attach hover and click events to glyphs and non-radial points."""
        for glyph in self.glyphs:
            glyph.mousePressEvent = self._create_click_event(glyph)
            glyph.setAcceptHoverEvents(True)
            glyph.hoverEnterEvent = self._create_hover_event(glyph, entering=True)
            glyph.hoverLeaveEvent = self._create_hover_event(glyph, entering=False)
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
            # Handle BeatReversalGlyph children
        # Directly access reversal items and assign events
            if glyph.name == "Reversals" and hasattr(glyph, "reversal_items"):
                for color, text_item in glyph.reversal_items.items():
                    print(f"Assigning hover and click events to reversal: {color}")
                    text_item.mousePressEvent = self._create_click_event(text_item)
                    text_item.hoverEnterEvent = self._create_hover_event(
                        text_item, entering=True
                    )
                    text_item.hoverLeaveEvent = self._create_hover_event(
                        text_item, entering=False
                    )
                    
        self.non_radial_points.mousePressEvent = self._create_non_radial_click_event()
        self.non_radial_points.hoverEnterEvent = self._create_hover_event(
            self.non_radial_points, entering=True
        )
        self.non_radial_points.hoverLeaveEvent = self._create_hover_event(
            self.non_radial_points, entering=False
        )

    def _create_hover_event(
        self, item: Union["NonRadialGridPoints", Glyph], entering: bool
    ):
        """Create a hover event for entering or leaving."""

        def hoverEvent(event):
            if item.name == "non_radial_points":
                children = item.childItems()
                for child in children:
                    child.setCursor(Qt.CursorShape.PointingHandCursor)
                item.setOpacity(
                    0.5
                    if entering
                    else (1 if self.settings.get_grid_visibility(item.name) else 0.1)
                )
            else:
                item.setCursor(Qt.CursorShape.PointingHandCursor)
                item.setOpacity(
                    0.5
                    if entering
                    else (
                        1
                        if self.settings.glyph.should_glyph_be_visible(item.name)
                        else 0.1
                    )
                )
                for child in item.childItems():
                    child.setCursor(Qt.CursorShape.PointingHandCursor)

        return hoverEvent

    def _create_click_event(self, glyph: Glyph):
        """Create a click event for toggling glyph visibility."""

        def clickEvent(event):
            current_visibility = self.settings.glyph.should_glyph_be_visible(glyph.name)
            self.settings.set_glyph_visibility(glyph.name, not current_visibility)
            glyph.setOpacity(1 if not current_visibility else 0.1)
            self.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent

    def _create_non_radial_click_event(self):
        """Create a click event for toggling non-radial points visibility."""

        def clickEvent(event):
            current_visibility = self.settings.grid.non_radial_visible
            self.settings.grid.set_non_radial_visibility(not current_visibility)
            self.non_radial_points.setOpacity(1 if not current_visibility else 0.1)
            self.visibility_tab.checkbox_widget.update_checkboxes()

        return clickEvent

    def resizeEvent(self, event: QEvent):
        """Handle resizing of the pictograph view."""
        available_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.checkbox_widget.width()
        )
        size = int(available_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
