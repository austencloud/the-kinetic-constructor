from typing import TYPE_CHECKING, Union

from base_widgets.base_pictograph.base_pictograph import BasePictograph

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

