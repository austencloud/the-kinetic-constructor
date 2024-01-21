from PyQt6.QtWidgets import QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List
from Enums import LetterType
from constants import ANTI, COLOR, DASH, MOTION_TYPE, PRO, STATIC
from utilities.TypeChecking.TypeChecking import Letters
from widgets.turns_box.turns_box import TurnsBox
from widgets.factories.attr_box_factory import TurnsBoxFactory
from utilities.TypeChecking.letter_lists import (
    pro_letters,
    anti_letters,
    dash_letters,
    static_letters,
)

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab


class TurnsPanel(QFrame):
    def __init__(self, filter_tab: "FilterTab", attribute_type) -> None:
        super().__init__()
        self.filter_tab = filter_tab
        self.attribute_type = attribute_type
        self.turns_box_factory = TurnsBoxFactory(self)
        self.boxes: List[TurnsBox] = self.turns_box_factory.create_boxes()
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for box in self.boxes:
            self.layout.addWidget(box)
            box.setObjectName("AttrBox")
            if box.attribute_type != COLOR:
                box.setStyleSheet(
                    f"{ 
                        'border-right: 1px solid black;' if box != self.boxes[-1] else ''
                    }"
                )

    def resize_turns_panel(self) -> None:
        self.setMinimumWidth(
            self.filter_tab.width()
            - (self.filter_tab.attr_box_border_width * len(self.boxes))
        ) # DON'T DELETE - This allows for three turns boxes at once

        for box in self.boxes:
            box.resize_turns_box()

    def show_boxes_based_on_chosen_letters(
        self, selected_letters: List[Letters]
    ) -> None:
        relevant_selected_letters = []
        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            if letter_type == self.filter_tab.section.letter_type:
                relevant_selected_letters.append(letter)

        motion_type_mapping = {
            PRO: pro_letters,
            ANTI: anti_letters,
            DASH: dash_letters,
            STATIC: static_letters,
        }

        for box in self.boxes:
            if box.attribute_type == MOTION_TYPE:
                show_box = any(
                    letter in relevant_selected_letters
                    for letter in motion_type_mapping[box.motion_type]
                )
                if show_box:
                    box.show()
                else:
                    box.hide()