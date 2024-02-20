from functools import lru_cache
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtSvg import QSvgRenderer
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.pictograph.components.tka_glyph.tka_glyph import TKA_Glyph


class TurnsColumnHandler(QGraphicsItemGroup):
    def __init__(self, glyph: "TKA_Glyph"):
        super().__init__()
        self.glyph = glyph
        self.top_number_item = None
        self.bottom_number_item = None
        self.svg_path_prefix = "images/numbers/"
        self.blank_svg_path = "images/blank.svg"

    @lru_cache
    def load_number_svg(self, number: Union[int, float]) -> QGraphicsSvgItem:
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
        return None

    def convert_number_to_int_if_it_is_a_whole_number(
        self, number: Union[int, float]
    ) -> int:
        return int(number) if number == int(number) else number

    def set_number(self, number: Union[int, float], is_top: bool):
        new_item = self.load_number_svg(number)
        old_item = self.top_number_item if is_top else self.bottom_number_item

        if old_item:
            self.removeFromGroup(old_item)
            old_item.hide()

        if new_item:
            self.addToGroup(new_item)
            new_item.show()
            if is_top:
                self.top_number_item = new_item
            else:
                self.bottom_number_item = new_item

    def position_turns(self):
        reference_rect = (
            self.glyph.dash_handler.dash_item.sceneBoundingRect()
            if self.glyph.dash_handler.dash_item
            else self.glyph.letter_handler.letter_item.sceneBoundingRect()
        )
        letter_scene_rect = self.glyph.letter_handler.letter_item.sceneBoundingRect()

        base_pos_x = reference_rect.right() + 15

        high_pos_y = letter_scene_rect.top() - 5
        low_pos_y = (
            letter_scene_rect.bottom()
            - (
                self.bottom_number_item.boundingRect().height()
                if self.bottom_number_item
                else 0
            )
            + 5
        )

        if self.top_number_item:
            self.top_number_item.setPos(base_pos_x, high_pos_y)

        if self.bottom_number_item:
            adjusted_low_pos_y = low_pos_y if self.top_number_item else high_pos_y + 20
            self.bottom_number_item.setPos(base_pos_x, adjusted_low_pos_y)

    def update_turns(self, top_turn: Union[int, float], bottom_turn: Union[int, float]):
        self.set_number(top_turn, is_top=True)
        self.set_number(bottom_turn, is_top=False)
        self.position_turns()
