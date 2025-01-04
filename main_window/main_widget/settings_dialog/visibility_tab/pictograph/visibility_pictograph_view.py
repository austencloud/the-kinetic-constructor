from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtCore import QEvent
from typing import TYPE_CHECKING
from base_widgets.base_pictograph.pictograph_view import PictographView
from Enums.Enums import Glyph
from .visibility_pictograph_interaction_manager import (
    VisibilityPictographInteractionManager,
)

if TYPE_CHECKING:
    from .visibility_pictograph import VisibilityPictograph
    from ..visibility_tab import VisibilityTab


class VisibilityPictographView(PictographView):

    def __init__(
        self, visibility_tab: "VisibilityTab", pictograph: "VisibilityPictograph"
    ):
        self.visibility_tab = visibility_tab
        self.visibility_settings = visibility_tab.settings
        self.main_widget = visibility_tab.main_widget
        super().__init__(pictograph)
        self.pictograph = self._initialize_data()
        self.non_radial_points = self._collect_non_radial_points()
        self._update_opacity()

        self.interaction_manager = VisibilityPictographInteractionManager(self)
        self.setStyleSheet("border: 2px solid black;")
        
    def _initialize_data(self) -> "VisibilityPictograph":
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
        self.glyphs = self._collect_glyphs()
        for glyph in self.glyphs:
            glyph.setVisible(True)
        self.pictograph.grid.toggle_non_radial_points(True)

        return self.pictograph

    def _collect_glyphs(self) -> list[Glyph]:
        return [
            self.pictograph.tka_glyph,
            self.pictograph.vtg_glyph,
            self.pictograph.elemental_glyph,
            self.pictograph.start_to_end_pos_glyph,
            self.pictograph.reversal_glyph,
        ]

    def _collect_non_radial_points(self) -> QGraphicsItemGroup:
        return self.pictograph.grid.items.get(
            f"{self.pictograph.grid.grid_mode}_nonradial"
        )

    def _update_opacity(self):
        for glyph in self.glyphs:
            glyph.setOpacity(
                1 if self.visibility_settings.get_glyph_visibility(glyph.name) else 0.1
            )
        self.non_radial_points.setOpacity(
            1 if self.visibility_settings.get_non_radial_visibility() else 0.1
        )

    def resizeEvent(self, event: QEvent):
        available_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.checkbox_widget.width()
        )
        size = int(available_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
