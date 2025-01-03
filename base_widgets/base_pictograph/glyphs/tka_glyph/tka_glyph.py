from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsItemGroup
from PyQt6.QtSvgWidgets import QGraphicsSvgItem

from base_widgets.base_pictograph.glyphs.tka_glyph.base_glyph import BaseGlyph


if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class TKA_Glyph(QGraphicsItemGroup, BaseGlyph):
    letter_item: "QGraphicsSvgItem"

    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(name="TKA")  # Ensure MRO handles initialization
        self.pictograph = pictograph
        self.letter = None
        self.init_handlers()

    def boundingRect(self):
        return self.childrenBoundingRect()

    def init_handlers(self) -> None:
        from .handlers.tka_letter_handler import TKALetterHandler
        from .handlers.dash_handler import DashHandler
        from .handlers.dot_handler import DotHandler
        from .handlers.turns_column import TurnsColumn

        self.letter_handler = TKALetterHandler(self)
        self.dash_handler = DashHandler(self)
        self.dot_handler = DotHandler(self)
        self.turns_column = TurnsColumn(self)

    def update_tka_glyph(self, visibility=True) -> None:
        self.letter = self.pictograph.letter
        self.letter_handler.set_letter()
        if not self.letter:
            return
        from .handlers.utils import parse_turns_tuple_string

        turns_tuple = self.pictograph.get.turns_tuple()
        direction, top_turn, bottom_turn = parse_turns_tuple_string(turns_tuple)
        self.dot_handler.update_dots(direction)
        self.dash_handler.update_dash()

        self.turns_column.update_turns_column(top_turn, bottom_turn)
        visibility_manager = (
            self.pictograph.main_widget.main_window.settings_manager.visibility.glyph_visibility_manager
        )
        self.setVisible(
            visibility_manager.should_glyph_be_visible("TKA") if visibility else False
        )
