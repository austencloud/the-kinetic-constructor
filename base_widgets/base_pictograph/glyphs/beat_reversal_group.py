from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsItemGroup
from PyQt6.QtGui import QFont, QColor

from data.constants import BLUE, HEX_BLUE, HEX_RED, RED
from utilities.reversal_detector import ReversalDetector

if TYPE_CHECKING:
    from base_widgets.base_pictograph.pictograph import Pictograph


class BeatReversalGroup(QGraphicsItemGroup):
    name = "Reversals"

    def __init__(self, pictograph: "Pictograph"):
        super().__init__()
        self.pictograph = pictograph
        self.reversal_items: dict[str, QGraphicsTextItem] = {}
        self.create_reversal_symbols()

    def create_reversal_symbols(self):
        red_R = self._create_reversal_text_item(HEX_RED)
        blue_R = self._create_reversal_text_item(HEX_BLUE)

        self.addToGroup(red_R)
        self.addToGroup(blue_R)

        self.pictograph.addItem(self)

        self.pictograph.blue_reversal_symbol = blue_R
        self.pictograph.red_reversal_symbol = red_R

        self.reversal_items[RED] = red_R
        self.reversal_items[BLUE] = blue_R

        self.setVisible(False)

    def update_reversal_symbols(self, visible: bool = True):
        if visible:
            if self.pictograph.view.__class__.__name__ == "OptionView":
                json_loader = self.pictograph.main_widget.json_manager.loader_saver
                sequence_so_far = json_loader.load_current_sequence()
                if not self.pictograph.pictograph_data:
                    return
                reversal_dict = ReversalDetector.detect_reversal(
                    sequence_so_far, self.pictograph.pictograph_data
                )
                blue_visible = reversal_dict.get("blue_reversal", False)
                red_visible = reversal_dict.get("red_reversal", False)
                settings = self.pictograph.main_widget.settings_manager.visibility
                reversals_enabled = settings.get_glyph_visibility("Reversals")

                # Apply global visibility setting
                blue_visible = blue_visible and reversals_enabled
                red_visible = red_visible and reversals_enabled
            else:
                blue_visible = self.pictograph.blue_reversal
                red_visible = self.pictograph.red_reversal
        else:
            blue_visible = False
            red_visible = False

        self.reversal_items[BLUE].setVisible(blue_visible)
        self.reversal_items[RED].setVisible(red_visible)

        center_y = self.pictograph.height() / 2

        if blue_visible and red_visible:
            red_R = self.reversal_items[RED]
            blue_R = self.reversal_items[BLUE]
            total_height = (
                red_R.boundingRect().height() + blue_R.boundingRect().height()
            )
            red_R_y = -total_height / 2
            blue_R_y = red_R_y + red_R.boundingRect().height()
            red_R.setPos(0, red_R_y)
            blue_R.setPos(0, blue_R_y)
        elif blue_visible:
            blue_R = self.reversal_items[BLUE]
            blue_R_y = -blue_R.boundingRect().height() / 2
            blue_R.setPos(0, blue_R_y)
        elif red_visible:
            red_R = self.reversal_items[RED]
            red_R_y = -red_R.boundingRect().height() / 2
            red_R.setPos(0, red_R_y)

        self.setVisible(blue_visible or red_visible)

        x_position = 40
        self.setPos(x_position, center_y)

        # self.pictograph.update()

    def _create_reversal_text_item(self, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem("R")
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
