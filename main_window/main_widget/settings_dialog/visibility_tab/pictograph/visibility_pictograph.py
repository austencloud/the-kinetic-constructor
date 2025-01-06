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

    def __init__(self, main_widget):
        super().__init__(main_widget)
        self.main_widget = main_widget
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            self.example_data
        )
        self.visibility_settings = self.main_widget.settings_manager.visibility
        self.red_reversal = True
        self.blue_reversal = True
        self.updater.update_pictograph(pictograph_dict)
        self.glyphs = self.get.glyphs()
        for glyph in self.glyphs:
            glyph.setVisible(True)
            glyph.setOpacity(
                1 if self.visibility_settings.get_glyph_visibility(glyph.name) else 0.1
            )
        self.grid.toggle_non_radial_points(True)
        self.non_radial_points = self.grid.items.get(f"{self.grid.grid_mode}_nonradial")
        self.non_radial_points.setOpacity(
            1 if self.visibility_settings.get_non_radial_visibility() else 0.1
        )
