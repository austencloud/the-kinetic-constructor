from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsRectItem
from PyQt6.QtGui import QPen

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..glyph import Glyph


class Dash:
    def __init__(self, glyph: "Glyph") -> None:
        self.glyph = glyph

    def add_dash_outline(self):
        dash_path = "images/dash.svg"
        dash_renderer = QSvgRenderer(dash_path)
        if dash_renderer.isValid():
            temp_dash_item = QGraphicsSvgItem()
            temp_dash_item.setSharedRenderer(dash_renderer)
            dash_width = temp_dash_item.boundingRect().width()

            dash_rect = QRectF(
                self.glyph.boundingRect().right(),
                self.glyph.boundingRect().top()
                + (
                    self.glyph.boundingRect().height()
                    - temp_dash_item.boundingRect().height()
                )
                / 2,
                dash_width,
                temp_dash_item.boundingRect().height(),
            )
            dash_outline = QGraphicsRectItem(dash_rect, self.glyph)
            dash_outline.setPen(QPen(Qt.GlobalColor.black, 1, Qt.PenStyle.SolidLine))
            dash_outline.setBrush(Qt.GlobalColor.transparent)
            dash_outline.setToolTip("Outline for Dash")

    def add_dash(self):
        dash_path = "images/dash.svg"
        dash_renderer = QSvgRenderer(dash_path)
        if dash_renderer.isValid():
            self.dash_item = QGraphicsSvgItem(self.glyph)
            self.dash_item.setSharedRenderer(dash_renderer)

            dash_x = self.glyph.boundingRect().width()
            dash_y = (
                self.glyph.boundingRect().height() / 2
                - self.dash_item.boundingRect().height() / 2
            )
            self.dash_item.setPos(QPointF(dash_x, dash_y))

    def position_item(self):
        dash_x = (
            self.glyph.vbox_frame.boundingRect().right()
        )  # Positioned right after the letter frame
        dash_y = (
            self.glyph.vbox_frame.boundingRect().height() / 2
            - self.dash_item.boundingRect().height() / 2
        )
        self.dash_item.setPos(dash_x, dash_y)
