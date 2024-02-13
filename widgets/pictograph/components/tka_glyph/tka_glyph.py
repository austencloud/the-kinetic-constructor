from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup

from .handlers.tka_letter_handler import TKALetterHandler
from .handlers.dash_handler import DashHandler
from .handlers.dot_handler import DotHandler
from .handlers.turns_column_handler import TurnsColumnHandler
from .handlers.utils import parse_turns_tuple_string

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class TKA_Glyph(QGraphicsItemGroup):
    def __init__(self, pictograph: "Pictograph"):
        super().__init__()
        self.pictograph = pictograph
        self.letter = None
        self.init_handlers()

    def init_handlers(self):
        self.letter_handler = TKALetterHandler(self)
        self.dash_handler = DashHandler(self)
        self.dot_handler = DotHandler(self)
        self.turns_column_handler = TurnsColumnHandler(self)
        self.addToGroup(self.turns_column_handler)

    def update_glyph(self):
        if not self.letter:
            self.setup_base_letter()
        turns_tuple = self.pictograph.get.turns_tuple()
        direction, top_turn, bottom_turn = parse_turns_tuple_string(turns_tuple)
        self.dot_handler.update_dots(direction)
        self.turns_column_handler.update_turns(top_turn, bottom_turn)

    def setup_base_letter(self):
        self.letter = self.pictograph.letter
        self.letter_handler.set_letter()
        if "-" in self.pictograph.letter:
            self.dash_handler.update_dash()

    def convert_to_ints(self, top_turn):
        top_turn = int(top_turn) if top_turn == int(top_turn) else top_turn
        bottom_turn = (
            int(bottom_turn) if bottom_turn == int(bottom_turn) else bottom_turn
        )
        return top_turn, bottom_turn
