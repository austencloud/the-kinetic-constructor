from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtGui import QPen, QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.pictograph.components.glyph.glyph import Glyph

# Add additional imports as needed...


class TurnsColumn(QGraphicsItemGroup):
    def __init__(self, glyph: "Glyph"):
        super().__init__()
        self.glyph = glyph  # Add a reference to the Glyph instance
        self.top_number_item = None
        self.bottom_number_item = None
        self.svg_path_prefix = "images/numbers/"
        self.blank_svg_path = "images/blank.svg"  # Path to a blank SVG for zero turns

    def load_number_svg(self, number: float) -> QGraphicsSvgItem:
        # Check if the number is zero and assign the blank SVG if so
        svg_path = (
            self.blank_svg_path
            if number == 0
            else f"{self.svg_path_prefix}{number}.svg"
        )
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            number_item = QGraphicsSvgItem()
            number_item.setSharedRenderer(renderer)
            return number_item
        else:
            # Handle the case where the SVG is not valid
            return None

    def set_top_number(self, number: float):
        if self.top_number_item:
            self.removeFromGroup(self.top_number_item)
            # Optionally delete the old item or reuse it
        self.top_number_item = self.load_number_svg(number)
        if self.top_number_item:
            self.addToGroup(self.top_number_item)

    def set_bottom_number(self, number: float):
        if self.bottom_number_item:
            self.removeFromGroup(self.bottom_number_item)
            # Optionally delete the old item or reuse it
        self.bottom_number_item = self.load_number_svg(number)
        if self.bottom_number_item:
            self.addToGroup(self.bottom_number_item)

    def position_numbers(self, frame_rect: QRectF):
        # Assuming the numbers should be centered within their halves of the frame
        if self.top_number_item:
            top_x = (
                frame_rect.width() - self.top_number_item.boundingRect().width()
            ) / 2
            top_y = (frame_rect.height() / 4) - (
                self.top_number_item.boundingRect().height() / 2
            )
            self.top_number_item.setPos(QPointF(top_x, top_y))

        if self.bottom_number_item:
            bottom_x = (
                frame_rect.width() - self.bottom_number_item.boundingRect().width()
            ) / 2
            bottom_y = (3 * frame_rect.height() / 4) - (
                self.bottom_number_item.boundingRect().height() / 2
            )
            self.bottom_number_item.setPos(QPointF(bottom_x, bottom_y))

    def update_turns(self, top_turn: float, bottom_turn: float, frame_rect: QRectF):
        self.set_top_number(top_turn)
        self.set_bottom_number(bottom_turn)
        self.position_numbers(frame_rect)
