from PyQt6.QtWidgets import QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List
from Enums import LetterNumberType
from constants import ANTI, COLOR, DASH, MOTION_TYPE, PRO, STATIC
from utilities.TypeChecking.TypeChecking import Letters
from widgets.attr_box.attr_box import AttrBox
from widgets.factories.attr_box_factory import AttrBoxFactory
from utilities.TypeChecking.letter_lists import (
    pro_letters,
    anti_letters,
    dash_letters,
    static_letters,
)

if TYPE_CHECKING:
    from widgets.filter_tab import FilterTab


class AttrPanel(QFrame):
    def __init__(self, filter_tab: "FilterTab", attribute_type) -> None:
        super().__init__()
        self.filter_tab = filter_tab
        self.attribute_type = attribute_type
        self.attr_box_factory = AttrBoxFactory(self)
        self.boxes: List[AttrBox] = self.attr_box_factory.create_boxes()
        self.setup_layouts()

    def setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        for box in self.boxes:
            self.layout.addWidget(box)
            box.setObjectName("AttrBox")
            if box.attribute_type != COLOR:
                box.setStyleSheet(
                    f"#AttrBox {{ "
                    f"border: 1px solid black;"
                    f" border-style: inset; "
                    f"}}"
                )

    def resize_attr_panel(self) -> None:
        self.setMinimumWidth(
            self.filter_tab.width()
            - (self.filter_tab.attr_box_border_width * len(self.boxes))
        )

        for box in self.boxes:
            box.resize_attr_box()

    def show_boxes_based_on_chosen_letters(
        self, selected_letters: List[Letters]
    ) -> None:
        # First, filter the selected letters by the current letter type
        # relevant_selected_letters = [
        #     letter for letter in selected_letters if letter.letter_type == self.filter_tab.section.letter_type
        # ]

        relevant_selected_letters = []

        for letter in selected_letters:
            letter_type = self.get_letter_type(letter)
            if letter_type == self.filter_tab.section.letter_type:
                relevant_selected_letters.append(letter)

        # Then, show or hide boxes based on the filtered selected letters
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

    def get_letter_type(self, str: str) -> str | None:
        for letter_type in LetterNumberType:
            if str in letter_type.letters:
                return letter_type.name.replace("_", "").lower().capitalize()
        return None
