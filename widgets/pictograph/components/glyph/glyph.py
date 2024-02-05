import ast
from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPen, QColor
from Enums import LetterType
from constants import Type3, Type5
from utilities.TypeChecking.TypeChecking import VtgDirections
from widgets.pictograph.components.glyph.parts.dash import DashHandler
from widgets.pictograph.components.glyph.parts.dot import DotHandler
from widgets.pictograph.components.glyph.parts.letter import LetterHandler
from typing import TYPE_CHECKING
from widgets.pictograph.components.glyph.parts.turns_column import TurnsColumnHandler

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class GlyphManager(QGraphicsItemGroup):
    letter: str = None
    """
    A Glyph is the combination of the current letter and its modifying components (dash, dot, and turns).

    This class manages the handlers for each of those components.

    Attributes:
        pictograph (Pictograph)
        letter_handler (LetterHandler)
        dash_handler (DashHandler)
        dot_handler (DotHandler)
        turns_column_handler (TurnsColumnHandler)


    Methods:
        init_components(): Initializes the glyph components.
        construct_frames(): Sets up the visual frames and calls setup methods for each component.
        parse_turns_tuple(turns_str: str): Parses a string representation of turns into a list.
        update_glyph(): Updates the glyph to reflect changes in the underlying pictograph data.
    """

    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.init_components()
        self._setup_dots()

    def init_components(self):
        self.letter_handler = LetterHandler(self)
        self.dash_handler = DashHandler(self)
        self.dot_handler = DotHandler(self)
        self.turns_column_handler = TurnsColumnHandler(self)
        self.addToGroup(
            self.turns_column_handler
        )

    def _setup_dots(self):
        self.dot_handler.add_dots("images/same_opp_dot.svg", "images/same_opp_dot.svg")

    def add_letter(self):
        self.letter = self.pictograph.letter
        self.letter_handler.render()
        self.letter_handler.position_letter()
        if LetterType.get_letter_type(self.pictograph.letter) in [Type3, Type5]:
            self.dash_handler.add_dash()
            self.dash_handler.position_dash()

    def parse_turns_tuple(self, turns_str: str):
        parts = turns_str.strip("()").split(",")
        turns_list = []

        for item in parts:
            item = item.strip()  # Strip extra spaces
            if item in ["0.5", "1.5", "2.5"]:
                item = float(item)
            elif item in ["0", "1", "2", "3"]:
                item = int(item)
            elif item == "s":
                item = VtgDirections.SAME
            elif item == "o":
                item = VtgDirections.OPP
            turns_list.append(item)

        return turns_list

    def update_glyph(self):
        turns_str = (
            self.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
                self.pictograph
            )
        )
        turns_list = self.parse_turns_tuple(turns_str)
        if len(turns_list) == 3:
            dir = turns_list[0]
            primary_turn = turns_list[1]
            secondary_turn = turns_list[2]
        elif len(turns_list) == 2:
            dir = None
            primary_turn = turns_list[0]
            secondary_turn = turns_list[1]
        self.turns_column_handler.update_turns(primary_turn, secondary_turn)
        self.dot_handler.toggle_dots(dir)
        if not self.letter:
            self.add_letter()


