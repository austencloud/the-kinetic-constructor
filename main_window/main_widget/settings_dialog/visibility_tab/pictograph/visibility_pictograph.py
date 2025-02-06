from typing import TYPE_CHECKING
from base_widgets.base_pictograph.base_pictograph import BasePictograph

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )
    from .visibility_pictograph_view import VisibilityPictographView


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

    def __init__(self, tab: "VisibilityTab"):
        super().__init__(tab.main_widget)
        self.tab = tab
        self.main_widget = tab.main_widget
        pictograph_dict = self.main_widget.pictograph_dict_loader.find_pictograph_dict(
            self.example_data
        )
        self.settings = self.main_widget.settings_manager.visibility
        self.updater.update_pictograph(pictograph_dict)
        self.glyphs = self.get.glyphs()
        for glyph in self.glyphs:
            glyph.setVisible(True)
            self.update_opacity(glyph.name, True)
        self.grid.toggle_non_radial_points(True)
        self.update_opacity("non_radial_points", True)
        
    def update_opacity(self, glyph_name: str, state: bool):
        """Animate the opacity of the corresponding glyph."""
        
        target_opacity = 1.0 if state else 0.1
        for glyph in self.glyphs:
            if glyph.name == glyph_name:
                self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                    glyph, target_opacity
                )

        if glyph_name == "non_radial_points":
            non_radial_points = self.grid.items.get(f"{self.grid.grid_mode}_nonradial")
            if non_radial_points:
                self.main_widget.fade_manager.widget_fader.fade_visibility_items_to_opacity(
                    non_radial_points, target_opacity
                )
