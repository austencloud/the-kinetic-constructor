import ast
from PyQt6.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem
from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPen, QColor
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

    def construct_master_frame(self, vbox_height, dash_width, turns_width):
        master_frame_width = self.boundingRect().width() + dash_width + turns_width
        self.master_frame = QGraphicsRectItem(
            QRectF(0, 0, master_frame_width, vbox_height), self
        )
        self.master_frame.setPen(QPen(QColor(0, 0, 0, 0)))

    def construct_letter_frame(self, vbox_height):
        self.vbox_frame = QGraphicsRectItem(
            QRectF(0, 0, self.boundingRect().width(), vbox_height), self.master_frame
        )
        self.vbox_frame.setPen(QPen(QColor(0, 0, 0, 0)))

    def construct_dash_frame(self, dash_width):
        dash_x = self.boundingRect().width()
        self.dash_frame = QGraphicsRectItem(
            QRectF(dash_x, 0, dash_width, self.boundingRect().height()),
            self.master_frame,
        )
        self.dash_frame.setPen(QPen(QColor(0, 0, 0, 0)))

    def construct_turns_frame(self, turns_width):
        turns_x = self.boundingRect().width() + self.dash_frame.boundingRect().width()
        self.turns_frame = QGraphicsRectItem(
            QRectF(turns_x, 0, turns_width, self.boundingRect().height()),
            self.master_frame,
        )
        self.turns_frame.setPen(QPen(QColor(0, 0, 0, 0)))

    def construct_frames(self):
        dash_width = 50
        turns_width = 100
        letter_frame_height = self.pictograph.height()
        self.construct_master_frame(letter_frame_height, dash_width, turns_width)
        self.construct_letter_frame(letter_frame_height)
        self.construct_dash_frame(dash_width)
        self.construct_turns_frame(turns_width)

        self._setup_dash()
        self._setup_dots()
        self._add_items_to_group()
        self.parse_and_create_turns()

    def _setup_dash(self):
        self.dash.add_dash()

    def _setup_dots(self):
        self.dot.add_dots("images/same_opp_dot.svg", "images/same_opp_dot.svg")

    def _add_letter(self):
        self.letter.render()
        self.letter.position_item()

    def _add_items_to_group(self):
        self.addToGroup(self.master_frame)
        self.addToGroup(self.vbox_frame)
        self.addToGroup(self.dash_frame)
        self.addToGroup(self.turns_column)

    def parse_and_create_turns(self):
        pass

    def update_turns_display(self, top_turn: float, bottom_turn: float):
        self.turns_column.update_turns(
            top_turn, bottom_turn, self.turns_frame.boundingRect()
        )

    def parse_turns_tuple(self, turns_str: str):
        # Remove parenthesis and split by comma
        parts = turns_str.strip("()").split(",")
        turns_list = []
        if len(parts) == 3:
            for item in parts:
                if item in ["0.5", "1.5", "2.5"]:
                    item = float(item)
                elif item in ["0", "1", "2", "3"]:
                    item = int(item)
                elif item == 's':
                    item = VtgDirections.SAME
                elif item == 'o':
                    item = VtgDirections.OPP
                turns_list.append(item)
        else:
            turns_list = parts
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
            self.dot.position_dots(dir)
        elif len(turns_list) == 2:
            primary_turn = turns_list[0]
            secondary_turn = turns_list[1]

        self._add_letter()
        self.update_turns_display(primary_turn, secondary_turn)
