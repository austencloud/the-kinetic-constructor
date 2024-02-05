from typing import TYPE_CHECKING, Tuple, Optional
from PyQt6.QtWidgets import QGraphicsItemGroup

from .handlers.letter_handler import LetterHandler
from .handlers.dash_handler import DashHandler
from .handlers.dot_handler import DotHandler
from .handlers.turns_column_handler import TurnsColumnHandler
from utilities.TypeChecking.TypeChecking import VtgDirections

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class GlyphManager(QGraphicsItemGroup):
    def __init__(self, pictograph: "Pictograph"):
        super().__init__()
        self.pictograph = pictograph
        self.letter = None
        self.init_handlers()

    def init_handlers(self):
        self.letter_handler = LetterHandler(self)
        self.dash_handler = DashHandler(self)
        self.dot_handler = DotHandler(self)
        self.turns_column_handler = TurnsColumnHandler(self)
        self.addToGroup(self.turns_column_handler)  # Assuming it's not already implicitly added

    def update_glyph(self):
        if not self.letter:
            self.setup_base_letter()

        turns_tuple = (
            self.pictograph.get.turns_tuple()
        )  # Assuming a method to fetch the turns tuple
        direction, top_turn, bottom_turn = self.parse_turns_tuple(turns_tuple)
        self.dot_handler.update_dots(direction)
        self.turns_column_handler.update_turns(top_turn, bottom_turn)

    def setup_base_letter(self):
        self.letter = self.pictograph.letter
        self.letter_handler.set_letter()
        if "-" in self.pictograph.letter:
            self.dash_handler.update_dash()

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
        if len(turns_list) == 3:
            return turns_list[0], turns_list[1], turns_list[2]
        else:
            return None, turns_list[0], turns_list[1]

    def convert_to_ints(self, top_turn):
        top_turn = int(top_turn) if top_turn == int(top_turn) else top_turn
        bottom_turn = (
            int(bottom_turn) if bottom_turn == int(bottom_turn) else bottom_turn
        )

        return top_turn, bottom_turn


# class GlyphManager(QGraphicsItemGroup):
#     letter: str = None
#     """
#     A Glyph is the combination of the current letter and its modifying components (dash, dot, and turns).

#     This class manages the handlers for each of those components.

#     Attributes:
#         pictograph (Pictograph)
#         letter_handler (LetterHandler)
#         dash_handler (DashHandler)
#         dot_handler (DotHandler)
#         turns_column_handler (TurnsColumnHandler)


#     Methods:
#         init_components(): Initializes the glyph components.
#         construct_frames(): Sets up the visual frames and calls setup methods for each component.
#         parse_turns_tuple(turns_str: str): Parses a string representation of turns into a list.
#         update_glyph(): Updates the glyph to reflect changes in the underlying pictograph data.
#     """

#     def __init__(self, pictograph: "Pictograph") -> None:
#         super().__init__()
#         self.pictograph = pictograph
#         self.init_components()
#         self._setup_dots()

#     def init_components(self):
#         self.letter_handler = LetterHandler(self)
#         self.dash_handler = DashHandler(self)
#         self.dot_handler = DotHandler(self)
#         self.turns_column_handler = TurnsColumnHandler(self)
#         self.addToGroup(self.turns_column_handler)

#     def _setup_dots(self):
#         self.dot_handler.add_dots("images/same_opp_dot.svg", "images/same_opp_dot.svg")

#     def add_letter(self):
#         self.letter = self.pictograph.letter
#         self.letter_handler.render()
#         self.letter_handler.position_letter()
#         if LetterType.get_letter_type(self.pictograph.letter) in [Type3, Type5]:
#             self.dash_handler.add_dash()
#             self.dash_handler.position_dash()

#     def parse_turns_tuple(self, turns_str: str):
#         parts = turns_str.strip("()").split(",")
#         turns_list = []

#         for item in parts:
#             item = item.strip()  # Strip extra spaces
#             if item in ["0.5", "1.5", "2.5"]:
#                 item = float(item)
#             elif item in ["0", "1", "2", "3"]:
#                 item = int(item)
#             elif item == "s":
#                 item = VtgDirections.SAME
#             elif item == "o":
#                 item = VtgDirections.OPP
#             turns_list.append(item)

#         return turns_list

#     def update_glyph(self):
#         turns_str = (
#             self.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
#                 self.pictograph
#             )
#         )
#         turns_list = self.parse_turns_tuple(turns_str)
#         if len(turns_list) == 3:
#             dir = turns_list[0]
#             primary_turn = turns_list[1]
#             secondary_turn = turns_list[2]
#         elif len(turns_list) == 2:
#             dir = None
#             primary_turn = turns_list[0]
#             secondary_turn = turns_list[1]
#         self.turns_column_handler.update_turns(primary_turn, secondary_turn)
#         self.dot_handler.toggle_dots(dir)
#         if not self.letter:
#             self.add_letter()
