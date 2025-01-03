from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING

from Enums.Enums import LetterType
from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph
from data.constants import (
    QUARTER_OPP,
    QUARTER_SAME,
    SPLIT_OPP,
    SPLIT_SAME,
    TOG_OPP,
    TOG_SAME,
)
from utilities.path_helpers import get_images_and_data_path


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


SVG_PATHS = {
    SPLIT_SAME: "water.svg",
    SPLIT_OPP: "fire.svg",
    TOG_SAME: "earth.svg",
    TOG_OPP: "air.svg",
    QUARTER_SAME: "sun.svg",
    QUARTER_OPP: "moon.svg",
}

SVG_BASE_PATH = get_images_and_data_path("images/elements")
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class ElementalGlyph(QGraphicsSvgItem, BaseGlyph):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(name="Elemental")
        self.pictograph = pictograph

    def set_elemental_glyph(self) -> None:
        if not self.pictograph.letter_type in [LetterType.Type1]:
            self.pictograph.removeItem(self)
            return
        vtg_mode = self.pictograph.vtg_mode
        svg_path: str = SVG_PATHS.get(vtg_mode, "")
        if not svg_path:
            return
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            if not self.scene():
                self.pictograph.addItem(self)
            self.position_elemental_glyph()
            visibility_manager = (
                self.pictograph.main_widget.main_window.settings_manager.visibility.glyph
            )
            self.setVisible(visibility_manager.should_glyph_be_visible("Elemental"))

    def position_elemental_glyph(self) -> None:
        pictograph_width = self.pictograph.width()
        pictograph_height = self.pictograph.height()

        offset_percentage = 0.04
        offset_width = pictograph_width * offset_percentage
        offset_height = pictograph_height * offset_percentage

        width = self.boundingRect().width()
        height = self.boundingRect().height()

        x = pictograph_width - width - offset_width
        y = offset_height
        self.setPos(x, y)
        self.setTransformOriginPoint(width / 2, height / 2)

    def update_elemental_glyph(self) -> None:
        self.set_elemental_glyph()
        self.position_elemental_glyph()
        visibility_manager = (
            self.pictograph.main_widget.main_window.settings_manager.visibility.glyph
        )
        self.setVisible(visibility_manager.should_glyph_be_visible("Elemental"))
