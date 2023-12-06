from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class LetterItem(QGraphicsSvgItem):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph

    def position_letter_item(self, letter_item: "QGraphicsSvgItem") -> None:
        x = (
            self.pictograph.width() / 2
            - letter_item.boundingRect().width() / 2
        )
        y = self.pictograph.width()
        letter_item.setPos(x, y)
