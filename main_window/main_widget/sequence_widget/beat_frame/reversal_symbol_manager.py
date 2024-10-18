# reversal_symbol_manager.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsTextItem
from PyQt6.QtGui import QFont, QColor

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView


class ReversalSymbolManager:
    def __init__(self, beat_view: "BeatView"):
        self.beat_view = beat_view
        self.scene = beat_view.scene()
        self.reversal_items = []

    def add_reversal_symbols(self):
        # Remove existing reversal symbols if any
        self.remove_reversal_symbols()

        beat = self.beat_view.beat
        if not beat:
            return

        reversal_items = []
        if beat.blue_reversal and beat.red_reversal:
            # Both hands reversed
            # Create two 'R's stacked vertically
            red_R = self._create_reversal_text_item("R", color="#ED1C24")
            blue_R = self._create_reversal_text_item("R", color="#2E3192")

            # Position them to the left of the grid
            total_height = (
                red_R.boundingRect().height() + blue_R.boundingRect().height()
            )
            # Decide the x position to the left of the grid
            x_position = 40  # Adjust as needed

            self.scene = self.beat_view.beat
            red_R.setPos(x_position, (self.scene.height() - total_height) / 2)
            blue_R.setPos(
                x_position,
                (self.scene.height() - total_height) / 2
                + red_R.boundingRect().height(),
            )

            self.scene.addItem(red_R)
            self.scene.addItem(blue_R)
            reversal_items.extend([red_R, blue_R])

        elif beat.blue_reversal or beat.red_reversal:
            # Only one hand reversed
            color = "blue" if beat.blue_reversal else "red"
            single_R = self._create_reversal_text_item("R", color=color)

            # Position the 'R' to the left of the grid
            x_position = 25  # Adjust as needed

            single_R.setPos(
                x_position, (self.scene.height() - single_R.boundingRect().height()) / 2
            )

            self.scene.addItem(single_R)
            reversal_items.append(single_R)

        # Store the reversal items for later removal
        self.reversal_items = reversal_items

    def remove_reversal_symbols(self) -> None:
        for item in self.reversal_items:
            self.scene.removeItem(item)
        self.reversal_items = []

    def _create_reversal_text_item(self, text, color) -> QGraphicsTextItem:
        text_item = QGraphicsTextItem(text)
        font = QFont("Georgia", 60, QFont.Weight.Bold)
        text_item.setFont(font)
        text_item.setDefaultTextColor(QColor(color))
        return text_item
