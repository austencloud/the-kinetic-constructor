from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPen

from Enums import LetterType
from typing import TYPE_CHECKING

from constants import Type1, Type2, Type3, Type4, Type5, Type6

if TYPE_CHECKING:
    from ..glyph import Glyph


class Letter:
    def __init__(self, glyph: "Glyph") -> None:
        self.glyph = glyph
        self.letter_item = QGraphicsSvgItem(self.glyph)
        self.renderer = None

    def render(self) -> None:
        if not self.glyph.pictograph.letter:
            return
        letter_type = LetterType.get_letter_type(self.glyph.pictograph.letter)
        if letter_type in [Type1, Type2, Type4, Type6]:
            svg_path = f"images/letters_trimmed/{letter_type}/{self.glyph.pictograph.letter}.svg"
        elif letter_type == Type3:
            svg_path = (
                f"images/letters_trimmed/Type2/{self.glyph.pictograph.letter[0]}.svg"
            )
        elif letter_type == Type5:
            svg_path = (
                f"images/letters_trimmed/Type4/{self.glyph.pictograph.letter[0]}.svg"
            )

        self.renderer = QSvgRenderer(svg_path)
        if self.renderer.isValid():
            self.letter_item.setSharedRenderer(self.renderer)
            self.add_outline()

    def add_outline(self) -> None:
        rect = self.letter_item.boundingRect()
        outline = QGraphicsRectItem(QRectF(rect), self.letter_item)
        outline.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        outline.setBrush(Qt.GlobalColor.transparent)
        outline.setToolTip("Outline for Letter")

    def position_item(self) -> None:
        x = int(self.letter_item.boundingRect().height() / 2)
        y = int(
            self.glyph.pictograph.height()
            - (self.letter_item.boundingRect().height() * 1.5)
        )
        self.letter_item.setPos(x, y)
