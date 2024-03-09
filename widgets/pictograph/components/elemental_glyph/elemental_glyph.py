from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING

from Enums.Enums import LetterType, VTG_Modes


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph

SVG_PATHS = {
    VTG_Modes.SPLIT_SAME: "water.svg",
    VTG_Modes.SPLIT_OPP: "fire.svg",
    VTG_Modes.TOG_SAME: "earth.svg",
    VTG_Modes.TOG_OPP: "air.svg",
    VTG_Modes.QUARTER_SAME: "sun.svg",
    VTG_Modes.QUARTER_OPP: "moon.svg",
}

SVG_BASE_PATH = "images/elements"
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class ElementalGlyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def set_elemental_glyph(self) -> None:
        if not self.pictograph.letter_type in [LetterType.Type1]:
            return
        vtg_mode = self.pictograph.vtg_mode
        svg_path: str = SVG_PATHS.get(vtg_mode, "")
        if not svg_path:
            return
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            self.pictograph.addItem(self)
            self.position_elemental_glyph()
            visibility_manager = (
                self.pictograph.main_widget.main_window.settings_manager.glyph_visibility_manager
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
