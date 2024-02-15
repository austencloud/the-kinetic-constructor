from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from typing import TYPE_CHECKING

from Enums.Enums import LetterType, VTG_Modes
from constants import SpecificPositions as SP


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph

SVG_PATHS = {
    VTG_Modes.SPLIT_SAME: "water.svg",
    VTG_Modes.SPLIT_OPP: "fire.svg",
    VTG_Modes.TOG_SAME: "earth.svg",
    VTG_Modes.TOG_OPP: "air.svg",
}

SVG_BASE_PATH = "images/elements"
SVG_PATHS = {
    vtg_mode: f"{SVG_BASE_PATH}/{path}" for vtg_mode, path in SVG_PATHS.items()
}


class ElementalGlyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def set_elemental_glyph(self):
        if not self.pictograph.letter_type in [LetterType.Type1]:
            return
        vtg_mode = self.pictograph.vtg_mode
        svg_path: str = SVG_PATHS.get(vtg_mode, "")
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            self.pictograph.addItem(self)
            self.position_elemental_glyph()
        print(f"SVG path: {svg_path}")  # Add this line for debug output

    def position_elemental_glyph(self) -> None:
        pictograph_width = self.pictograph.width()
        pictograph_height = self.pictograph.height()

        scale_factor = 0.5
        self.setScale(scale_factor)

        border_percentage = 0.03
        additional_margin_percentage = 0.03

        border_offset_width = pictograph_width * border_percentage
        border_offset_height = pictograph_height * border_percentage
        additional_margin_width = pictograph_width * additional_margin_percentage
        additional_margin_height = pictograph_height * additional_margin_percentage

        effective_pictograph_width = pictograph_width - 2 * (
            border_offset_width + additional_margin_width
        )

        scaled_width = self.boundingRect().width() * scale_factor
        scaled_height = self.boundingRect().height() * scale_factor

        x = (
            effective_pictograph_width
            - scaled_width
            + (border_offset_width + additional_margin_width)
        )
        y = border_offset_height + additional_margin_height

        y -= scaled_height / 3

        self.setPos(x, y)
        self.setTransformOriginPoint(scaled_width / 2, scaled_height / 2)

        print(f"ElementalGlyph positioned: {x}, {y}")
