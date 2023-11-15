from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from widgets.graphboard.graphboard import GraphBoard


class LetterItem(QGraphicsSvgItem):
    def __init__(self, graphboard: 'GraphBoard') -> None:
        super().__init__()
        self.graphboard = graphboard