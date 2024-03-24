from typing import TYPE_CHECKING
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from ..tka_glyph import TKA_Glyph


class DashHandler:
    def __init__(self, glyph: "TKA_Glyph") -> None:
        self.glyph = glyph
        self.dash_item = None

    def add_dash(self) -> None:
        dash_path = get_images_and_data_path("images/dash.svg")
        self.dash_item = self.create_dash(dash_path)
        self.glyph.addToGroup(self.dash_item)

    def create_dash(self, dash_path: str) -> QGraphicsSvgItem:
        renderer = QSvgRenderer(dash_path)
        if renderer.isValid():
            item = QGraphicsSvgItem()
            item.setSharedRenderer(renderer)
            return item
        return None

    def position_dash(self) -> None:
        padding = 5
        if self.dash_item:
            letter_scene_rect = (
                self.glyph.letter_handler.letter_item.sceneBoundingRect()
            )
            dash_x = letter_scene_rect.right() + padding
            dash_y = (
                letter_scene_rect.center().y()
                - self.dash_item.boundingRect().height() / 2
            )
            self.dash_item.setPos(dash_x, dash_y)

    def update_dash(self) -> None:
        self.add_dash()
        self.position_dash()
