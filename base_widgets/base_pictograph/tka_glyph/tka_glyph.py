from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup

from .handlers.tka_letter_handler import TKALetterHandler
from .handlers.dash_handler import DashHandler
from .handlers.dot_handler import DotHandler
from .handlers.turns_column_handler import TurnsColumnHandler
from .handlers.utils import parse_turns_tuple_string

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class TKA_Glyph(QGraphicsItemGroup):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.letter = None
        self.init_handlers()

    def init_handlers(self) -> None:
        self.letter_handler = TKALetterHandler(self)
        self.dash_handler = DashHandler(self)
        self.dot_handler = DotHandler(self)
        self.turns_column_handler = TurnsColumnHandler(self)
        self.addToGroup(self.turns_column_handler)

    def update_tka_glyph(self, visibility = True) -> None:
        self.letter = self.pictograph.letter
        self.letter_handler.set_letter()
        if not self.letter:
            return
        turns_tuple = self.pictograph.get.turns_tuple()
        direction, top_turn, bottom_turn = parse_turns_tuple_string(turns_tuple)
        self.dot_handler.update_dots(direction)
        self.dash_handler.update_dash()
        
        self.turns_column_handler.update_turns(top_turn, bottom_turn)
        visibility_manager = (
            self.pictograph.main_widget.main_window.settings_manager.visibility.glyph_visibility_manager
        )
        self.setVisible(visibility_manager.should_glyph_be_visible("TKA") if visibility else False)

    def convert_to_ints(self, top_turn) -> int:
        top_turn = int(top_turn) if top_turn == int(top_turn) else top_turn
        bottom_turn = (
            int(bottom_turn) if bottom_turn == int(bottom_turn) else bottom_turn
        )
        return top_turn, bottom_turn
