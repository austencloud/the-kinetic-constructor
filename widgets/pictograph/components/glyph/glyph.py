import ast
from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPen, QColor
from Enums import LetterType
from constants import Type3, Type5
from utilities.TypeChecking.TypeChecking import VtgDirections
from widgets.pictograph.components.glyph.parts.dash import Dash
from widgets.pictograph.components.glyph.parts.dot import Dot
from widgets.pictograph.components.glyph.parts.letter import Letter
from typing import TYPE_CHECKING
from widgets.pictograph.components.glyph.parts.turns_column import TurnsColumn

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class Glyph(QGraphicsItemGroup):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.init_components()
        self.construct_frames()

    def init_components(self):
        self.letter = Letter(self)
        self.dash = Dash(self)
        self.dot = Dot(self)
        self.turns_column = TurnsColumn(self)
        self.addToGroup(self.turns_column)  # Ensure the TurnsColumn is added to the Glyph

    def construct_frames(self):
        self._setup_dots()
        self.parse_and_create_turns()

    def _setup_dots(self):
        self.dot.add_dots("images/same_opp_dot.svg", "images/same_opp_dot.svg")

    def _add_letter(self):
        self.letter.render()
        self.letter.position_letter()

    def parse_and_create_turns(self):
        pass

    def parse_turns_tuple(self, turns_str: str):
        # Remove parenthesis and split by comma
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

        self.dot.toggle_dots(dir)

        self._add_letter()
        if LetterType.get_letter_type(self.pictograph.letter) in [Type3, Type5]:
            self.dash.add_dash()
            self.dash.position_dash()

        self.turns_column.update_turns(primary_turn, secondary_turn)
