from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import QEvent

from base_widgets.base_pictograph.pictograph_view import PictographView

if TYPE_CHECKING:
    from .visibility_tab_pictograph import VisibilityTabPictograph
    from .visibility_tab import VisibilityTab
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem
    from PyQt6.QtWidgets import QGraphicsItemGroup
    from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityTabPictographView(PictographView):
    """Manages interactions with pictograph view, delegating logic to managers."""

    def __init__(
        self, visibility_tab: "VisibilityTab", pictograph: "VisibilityTabPictograph"
    ):
        super().__init__(pictograph)
        self.visibility_tab = visibility_tab
        self.settings = visibility_tab.settings
        self.main_widget = visibility_tab.main_widget
        self.pictograph = pictograph
        self.pictograph.view = self

    def resizeEvent(self, event: QEvent):
        available_width = (
            self.visibility_tab.dialog.width()
            - self.visibility_tab.checkbox_widget.width()
        )
        size = int(available_width * 0.7)
        self.setFixedSize(size, size)
        super().resizeEvent(event)
