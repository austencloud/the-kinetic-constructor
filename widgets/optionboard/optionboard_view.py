from typing import TYPE_CHECKING

from settings.numerical_constants import RATIO

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGraphicsView

if TYPE_CHECKING:
    from widgets.optionboard.optionboard import OptionBoard

class OptionBoardView(QGraphicsView):
    def __init__(self, optionboard: "OptionBoard") -> None:
        super().__init__(optionboard)
    
        self.main_window = optionboard.main_widget.main_window
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setFixedSize(int(self.main_window.width()*0.5 * RATIO), int(self.main_window.width()*0.5))