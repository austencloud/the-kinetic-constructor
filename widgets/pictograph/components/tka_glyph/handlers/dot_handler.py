from PyQt6.QtCore import QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING
from .utils import load_svg_item

from Enums.Enums import VTG_Directions

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class DotHandler:
    def __init__(self, glyph: "TKA_Glyph") -> None:
        self.glyph = glyph
        self.same_dot_item = None
        self.opp_dot_item = None
        self.add_dots("images/same_opp_dot.svg")

    def add_dots(self, dot_path: str):
        self.same_dot_item = self.create_dot(dot_path)
        if self.same_dot_item:
            self.glyph.addToGroup(self.same_dot_item)

        self.opp_dot_item = self.create_dot(dot_path)
        if self.opp_dot_item:
            self.glyph.addToGroup(self.opp_dot_item)

    def create_dot(self, dot_path: str) -> QGraphicsSvgItem:
        return load_svg_item(dot_path)

    def update_dots(self, dir: VTG_Directions):
        padding = 0
        letter_scene_rect = self.glyph.letter_handler.letter_item.sceneBoundingRect()
        letter_scene_center = letter_scene_rect.center()

        if self.same_dot_item:
            same_dot_height = self.same_dot_item.boundingRect().height()
            same_dot_center = QPointF(
                letter_scene_center.x(),
                letter_scene_rect.top() - same_dot_height / 2 - padding,
            )
            self.same_dot_item.setPos(
                same_dot_center - self.same_dot_item.boundingRect().center()
            )

        if self.opp_dot_item:
            opp_dot_height = self.opp_dot_item.boundingRect().height()
            opp_dot_center = QPointF(
                letter_scene_center.x(),
                letter_scene_rect.bottom() + opp_dot_height / 2 + padding,
            )
            self.opp_dot_item.setPos(
                opp_dot_center - self.opp_dot_item.boundingRect().center()
            )

        if dir == VTG_Directions.SAME:
            self.same_dot_item.show()
            self.opp_dot_item.hide()
        elif dir == VTG_Directions.OPP:
            self.same_dot_item.hide()
            self.opp_dot_item.show()
        else:
            self.same_dot_item.hide()
            self.opp_dot_item.hide()
