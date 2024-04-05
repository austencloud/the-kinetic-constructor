from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from Enums.Enums import Letter

from .letterbook_letter_button_frame.letterbook_letter_button_frame import (
    LetterBookButtonFrame,
)
from .letterbook_scroll_area import LetterBookScrollArea
from ..pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class LetterBook(QWidget):
    selected_letters: list[Letter] = []

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.letters_dict = self.main_widget.letters

        self.pictograph_cache: dict[Letter, dict[str, Pictograph]] = {
            letter: {} for letter in Letter
        }
        self.scroll_area = LetterBookScrollArea(self)
        self.button_frame = LetterBookButtonFrame(self)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.scroll_area, 5)
        self.right_layout.addWidget(self.button_frame, 1)
        self.layout.addLayout(self.left_layout, 5)
        self.layout.addLayout(self.right_layout, 1)

    def resize_letterbook(self) -> None:
        self.button_frame.resize_letterbook_letter_button_frame()

    def update_pictographs(self) -> None:
        deselected_letters = (
            self.scroll_area.pictograph_factory.get_deselected_letters()
        )
        selected_letters = set(self.selected_letters)

        if self.scroll_area._only_deselection_occurred(
            deselected_letters, selected_letters
        ):
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(
                    letter
                )
        else:
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(
                    letter
                )
            self.scroll_area.pictograph_factory.process_selected_letters()
        for section in self.scroll_area.sections_manager.sections.values():
            self.scroll_area.display_manager.order_and_display_pictographs(section)
