
from .utils import load_svg_item
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..glyph import GlyphManager


class DashHandler:
    def __init__(self, glyph: "GlyphManager") -> None:
        self.glyph = glyph
        self.dash_item = None

    def add_dash(self):
        dash_path = "images/dash.svg"
        self.dash_item = load_svg_item(dash_path)
        self.glyph.addToGroup(self.dash_item)

    def position_dash(self):
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

    def update_dash(self):
        self.add_dash()
        self.position_dash()
