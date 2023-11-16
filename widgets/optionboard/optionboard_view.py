from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from widgets.optionboard.optionboard import OptionBoard

class OptionBoardView(QGraphicsView):
    def __init__(self, optionboard: "OptionBoard") -> None:
        super().__init__(optionboard)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFixedSize(int(self.sceneRect().width()), int(self.sceneRect().height()))