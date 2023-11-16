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
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # set the maximum height to 2/3 of the window height
        self.width = int(self.main_window.width() * 0.35)
        self.height = int(self.main_window.height() * (2 / 3))
        self.setMaximumHeight(self.height)
        self.setMaximumWidth(self.width)
