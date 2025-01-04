from PyQt6.QtWidgets import QGraphicsItemGroup
from typing import TYPE_CHECKING, Union
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph

if TYPE_CHECKING:
    from .visibility_tab_pictograph import VisibilityTabPictograph
    from PyQt6.QtSvgWidgets import QGraphicsSvgItem

Glyph = Union["BaseGlyph", "QGraphicsItemGroup", "QGraphicsSvgItem"]


class VisibilityManager:
    """Applies and updates visibility states for glyphs and non-radial points."""

    def __init__(self, pictograph: "VisibilityTabPictograph"):
        self.pictograph = pictograph
