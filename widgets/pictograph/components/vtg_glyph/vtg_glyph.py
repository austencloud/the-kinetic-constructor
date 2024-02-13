from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from Enums import LetterType
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


SVG_PATHS = {
    LetterType.Type1: "Type1/{letter}.svg",
    LetterType.Type2: "Type2/{letter}.svg",
    LetterType.Type3: "Type2/{letter[0]}.svg",
    LetterType.Type4: "Type4/{letter}.svg",
    LetterType.Type5: "Type4/{letter[0]}.svg",
    LetterType.Type6: "Type6/{letter}.svg",
}

SVG_BASE_PATH = "images/letters_trimmed"
SVG_PATHS = {
    letter_type: f"{SVG_BASE_PATH}/{path}" for letter_type, path in SVG_PATHS.items()
}


class VTG_Glyph:
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        # self.letter_item = QGraphicsSvgItem(self.glyph)
        self.renderer = None

    def set_vtg_mode(self):
        self.mode = self.pictograph.vtg_mode
        self.set_letter()

    def set_letter(self) -> None:
        if not self.pictograph.vtg_mode:
            return
        letter_type = LetterType.get_letter_type(self.glyph.pictograph.letter)
        self.pictograph.letter_type = letter_type
        svg_path: str = SVG_PATHS.get(letter_type, "")
        svg_path = svg_path.format(letter=self.glyph.pictograph.letter)
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.letter_item.setSharedRenderer(self.renderer)
            self.position_letter()

    def position_letter(self) -> None:
        x = int(self.letter_item.boundingRect().height() / 1.5)
        y = int(
            self.pictograph.height() - (self.letter_item.boundingRect().height() * 1.7)
        )
        self.letter_item.setPos(x, y)
