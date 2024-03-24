from PyQt6.QtCore import QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from typing import TYPE_CHECKING

from Enums.Enums import VTG_Directions
from constants import OPP, SAME
from path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class DotHandler:
    def __init__(self, glyph: "TKA_Glyph") -> None:
        self.glyph = glyph
        self.same_dot_item = None
        self.opp_dot_item = None
        self.add_dots(get_images_and_data_path("images/same_opp_dot.svg"))
        self.hide_dots()

    def add_dots(self, dot_path: str) -> None:
        self.same_dot_item = self.create_dot(dot_path)
        if self.same_dot_item:
            self.glyph.addToGroup(self.same_dot_item)

        self.opp_dot_item = self.create_dot(dot_path)
        if self.opp_dot_item:
            self.glyph.addToGroup(self.opp_dot_item)

    def hide_dots(self) -> None:
        self.same_dot_item.hide()
        self.opp_dot_item.hide()

    def create_dot(self, dot_path: str) -> QGraphicsSvgItem:
        renderer = QSvgRenderer(dot_path)
        if renderer.isValid():
            item = QGraphicsSvgItem()
            item.setSharedRenderer(renderer)
            return item
        else:
            # Handle the error or log a warning that the renderer could not be created
            print(f"Warning: Renderer for {dot_path} is not valid.")
            return None

    def update_dots(self, dir: VTG_Directions) -> None:
        padding = 10
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

        if dir == SAME:
            self.same_dot_item.show()
            self.opp_dot_item.hide()

        elif dir == OPP:
            self.same_dot_item.hide()
            self.opp_dot_item.show()

        else:
            self.same_dot_item.hide()
            self.opp_dot_item.hide()
