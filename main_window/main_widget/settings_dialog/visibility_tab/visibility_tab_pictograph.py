from typing import TYPE_CHECKING, Union

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from objects.grid import NonRadialGridPoints
from .glyph_manager import GlyphManager
from .grid_manager import GridManager
from .visibility_manager import VisibilityManager

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab_pictograph_view import (
        VisibilityTabPictographView,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem
    from PyQt6.QtWidgets import QGraphicsItemGroup
    from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityTabPictograph(BasePictograph):
    """Special class for the visibility tab pictograph."""

    example_data = {
        "letter": "A",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "blue_motion_type": "pro",
        "red_motion_type": "pro",
    }
    view: "VisibilityTabPictographView" = None
    red_reversal = True
    blue_reversal = True

    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.dict_loader = self.main_widget.pictograph_dict_loader

        self.glyph_manager = GlyphManager(self)
        self.grid_manager = GridManager(self)
        self.visibility_manager = VisibilityManager(self)

        pictograph_dict = self.dict_loader.find_pictograph_dict(self.example_data)
        self.updater.update_pictograph(pictograph_dict)
        for glyph in self.get.glyphs():
            glyph.setVisible(True)
        self.grid.toggle_non_radial_points_visibility(True)
        self.apply_initial_visibility()

    def apply_initial_visibility(self):
        """Set initial visibility for glyphs and non-radial points."""
        for glyph in self.glyph_manager.glyphs:
            glyph.setOpacity(
                1
                if self.main_widget.settings_manager.visibility.glyph.should_glyph_be_visible(
                    glyph.name
                )
                else 0.1
            )
        self.grid_manager.non_radial_points.setOpacity(
            1
            if self.main_widget.settings_manager.visibility.grid.non_radial_visible
            else 0.1
        )
