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
        self.dash_item = None

    def add_dash(self):
        dash_path = "images/dash.svg"
        dash_renderer = QSvgRenderer(dash_path)
        if dash_renderer.isValid():
            self.dash_item = QGraphicsSvgItem(self.glyph)
            self.dash_item.setSharedRenderer(dash_renderer)
            self.dash_item.setPos(0, 0)
            self.glyph.addToGroup(self.dash_item)

    def position_dash(self):
        padding = 5
        if self.dash_item:
            letter_scene_rect = self.glyph.letter.letter_item.sceneBoundingRect()
            dash_x = letter_scene_rect.right() + padding
            dash_y = (
                letter_scene_rect.center().y()
                - self.dash_item.boundingRect().height() / 2
            )
            self.dash_item.setPos(dash_x, dash_y)
