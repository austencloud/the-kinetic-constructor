# reversal_symbol_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor

from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class ReversalSymbolManager:
    def __init__(self, pictograph: "BasePictograph"):
        self.pictograph = pictograph
        self.reversal_items: dict[str, QGraphicsTextItem] = {}
        self.create_reversal_symbols()

    def create_reversal_symbols(self):
        # Create reversal symbols for both hands
        red_R = self._create_reversal_text_item("R", color=HEX_RED)
        blue_R = self._create_reversal_text_item("R", color=HEX_BLUE)

        # Position them appropriately
        total_height = red_R.boundingRect().height() + blue_R.boundingRect().height()
        x_position = 40  # Adjust as needed
        center_y = self.pictograph.height() / 2

        red_R.setPos(x_position, center_y - total_height / 2)
        blue_R.setPos(
            x_position, center_y - total_height / 2 + red_R.boundingRect().height()
        )

        # Add items to the pictograph
        self.pictograph.addItem(red_R)
        self.pictograph.addItem(blue_R)

        self.pictograph.blue_reversal_symbol = blue_R
        self.pictograph.red_reversal_symbol = red_R

        # Store references to the reversal items
        self.reversal_items[RED] = red_R
        self.reversal_items[BLUE] = blue_R

        # Initially hide the reversal symbols
        red_R.setVisible(False)
        blue_R.setVisible(False)

    def update_reversal_symbols(self):
        # Update the visibility of the reversal symbols based on the pictograph's reversal flags
        if self.pictograph.blue_reversal:
            self.reversal_items[BLUE].setVisible(True)
        else:
            self.reversal_items[BLUE].setVisible(False)

        if self.pictograph.red_reversal:
            self.reversal_items[RED].setVisible(True)
        else:
            self.reversal_items[RED].setVisible(False)
            
        self.pictograph.update()
        self.pictograph.view.update()
        

    def _create_reversal_text_item(self, text, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem(text)
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
