from typing import TYPE_CHECKING, Union

from base_widgets.base_pictograph.base_pictograph import BasePictograph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.pictograph.visibility_pictograph_view import (
        VisibilityPictographView,
    )
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem
    from PyQt6.QtWidgets import QGraphicsItemGroup
    from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityPictograph(BasePictograph):
    """Special class for the visibility tab pictograph."""

    example_data = {
        "letter": "A",
        "start_pos": "alpha1",
        "end_pos": "alpha3",
        "blue_motion_type": "pro",
        "red_motion_type": "pro",
    }
    view: "VisibilityPictographView" = None
    red_reversal = True
    blue_reversal = True

    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.main_widget = main_widget
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            self.example_data
        )
        self.settings = self.main_widget.settings_manager.visibility
        self.updater.update_pictograph(pictograph_dict)
        self.glyphs = self.get.glyphs()
        for glyph in self.glyphs:
            glyph.setVisible(True)
        self.grid.toggle_non_radial_points(True)
        for glyph in self.glyphs:
            self.update_opacity(
                glyph.name, self.settings.get_glyph_visibility(glyph.name)
            )
        self.update_opacity(
            "Non-radial points", self.settings.get_non_radial_visibility()
        )

    def update_opacity(self, glyph_name: str, state: bool):
        for glyph in self.glyphs:
            if glyph.name == glyph_name:
                glyph.setOpacity(1 if state else 0.1)
        if glyph_name == "Non-radial points":
            self.non_radial_points = self.grid.items.get(
                f"{self.grid.grid_mode}_nonradial"
            )
            self.non_radial_points.setOpacity(1 if state else 0.1)
