# reversal_symbol_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor

from data.constants import HEX_BLUE, HEX_RED
if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph

class ReversalSymbolManager:
    def __init__(self, pictograph: "BasePictograph"):
        self.pictograph = pictograph
        self.reversal_items = []

    def add_reversal_symbols(self):
        # Remove existing reversal symbols if any
        self.remove_reversal_symbols()

        if not self.pictograph:
            return

        reversal_items = []
        if self.pictograph.blue_reversal and self.pictograph.red_reversal:
            # Both hands reversed
            # Create two 'R's stacked vertically
            red_R = self._create_reversal_text_item('R', color=HEX_RED)
            blue_R = self._create_reversal_text_item('R', color=HEX_BLUE)

            # Position them appropriately (adjust positions as needed)
            total_height = red_R.boundingRect().height() + blue_R.boundingRect().height()
            x_position = 40  # Adjust as needed
            center_y = self.pictograph.height() / 2

            red_R.setPos(
                x_position,
                center_y - total_height / 2
            )
            blue_R.setPos(
                x_position,
                center_y - total_height / 2 + red_R.boundingRect().height()
            )

            self.pictograph.addItem(red_R)
            self.pictograph.addItem(blue_R)
            reversal_items.extend([red_R, blue_R])

        elif self.pictograph.blue_reversal or self.pictograph.red_reversal:
            # Only one hand reversed
            color = HEX_BLUE if self.pictograph.blue_reversal else HEX_RED
            single_R = self._create_reversal_text_item('R', color=color)

            # Position the 'R' to the left of the grid
            x_position = 40  # Adjust as needed

            single_R.setPos(
                x_position,
                (self.pictograph.height() - single_R.boundingRect().height()) / 2
            )

            self.pictograph.addItem(single_R)
            reversal_items.append(single_R)

        # Store the reversal items for later removal
        self.reversal_items = reversal_items

    def remove_reversal_symbols(self):
        for item in self.reversal_items:
            self.pictograph.removeItem(item)
        self.reversal_items = []

    def _create_reversal_text_item(self, text, color):
        text_item = QGraphicsTextItem(text)
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
