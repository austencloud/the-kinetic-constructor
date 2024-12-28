from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor

from data.constants import BLUE, HEX_BLUE, HEX_RED, RED

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class BeatReversalManager:
    def __init__(self, pictograph: "BasePictograph"):
        self.pictograph = pictograph
        self.reversal_items: dict[str, QGraphicsTextItem] = {}
        self.create_reversal_symbols()

    def create_reversal_symbols(self):
        # Create reversal symbols for both hands
        red_R = self._create_reversal_text_item(HEX_RED)
        blue_R = self._create_reversal_text_item(HEX_BLUE)

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
        blue_visible = self.pictograph.blue_reversal
        red_visible = self.pictograph.red_reversal

        self.reversal_items[BLUE].setVisible(blue_visible)
        self.reversal_items[RED].setVisible(red_visible)

        x_position = 40  # Adjust as needed
        center_y = self.pictograph.height() / 2

        if blue_visible and red_visible:
            # Both symbols are visible, position them stacked
            red_R = self.reversal_items[RED]
            blue_R = self.reversal_items[BLUE]
            total_height = (
                red_R.boundingRect().height() + blue_R.boundingRect().height()
            )
            red_R_y = center_y - total_height / 2
            blue_R_y = red_R_y + red_R.boundingRect().height()
            red_R.setPos(x_position, red_R_y)
            blue_R.setPos(x_position, blue_R_y)
        elif blue_visible:
            # Only blue symbol is visible, center it vertically
            blue_R = self.reversal_items[BLUE]
            blue_R_y = center_y - blue_R.boundingRect().height() / 2
            blue_R.setPos(x_position, blue_R_y)
        elif red_visible:
            # Only red symbol is visible, center it vertically
            red_R = self.reversal_items[RED]
            red_R_y = center_y - red_R.boundingRect().height() / 2
            red_R.setPos(x_position, red_R_y)
        # else: both are not visible, do nothing

        self.pictograph.update()
        # self.pictograph.view.update()

    def _create_reversal_text_item(self, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem("R")
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
