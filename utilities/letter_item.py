from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class LetterItem(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.letter = ""
        
    def position_letter_item(self, letter_item: "QGraphicsSvgItem") -> None:
        x = int(letter_item.boundingRect().height() / 2)
        y = int(self.pictograph.height() - (letter_item.boundingRect().height() * 1.5))
        letter_item.setPos(x, y)
