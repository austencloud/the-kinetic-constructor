from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer

from Enums import LetterType
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


# SVG_PATHS = {
#     pass: "pass.svg",
# }

# SVG_BASE_PATH = "images/letters_trimmed"
# SVG_PATHS = {
#     letter_type: f"{SVG_BASE_PATH}/{path}" for letter_type, path in SVG_PATHS.items()
# }


class VTG_Glyph(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        self.pictograph = pictograph
        self.letter_item = QGraphicsSvgItem(self.glyph)
        self.renderer = None

    def set_vtg_mode(self):
        self.mode = self.pictograph.vtg_mode
        self.set_letter()

    def set_letter(self) -> None:
        if not self.pictograph.vtg_mode:
            return
        letter_type = LetterType.get_letter_type(self.pictograph.letter)
        self.pictograph.letter_type = letter_type
        # svg_path: str = SVG_PATHS.get(letter_type, "")
        svg_path = svg_path.format(letter=self.pictograph.letter)
        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.setSharedRenderer(self.renderer)
            self.position_letter()

    def position_letter(self) -> None:
        x = int(self.boundingRect().height() / 1.5)
        y = int(self.pictograph.height() - (self.boundingRect().height() * 1.7))
        self.setPos(x, y)
