from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class LetterItem(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def position_letter_item(self, letter_item: "QGraphicsSvgItem") -> None:
        x = int(letter_item.boundingRect().width() * self.pictograph.view.view_scale)
        y = int(self.pictograph.height() - letter_item.boundingRect().height() - letter_item.boundingRect().height()/2)
        letter_item.setPos(x, y)
