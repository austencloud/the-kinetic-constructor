from Enums import LetterType
from typing import TYPE_CHECKING, List

from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtCore import QSize
from Enums import LetterType
from typing import Dict
from constants import LETTER_BTN_ICON_DIR
from utilities.TypeChecking.TypeChecking import Letters
from widgets.letter_button_frame.components.letter_button_click_handler import (
    LetterButtonClickHandler,
)
from widgets.letter_button_frame.components.letter_button_styler import (
    LetterButtonStyler,
)
from .letter_button import LetterButton

if TYPE_CHECKING:
    from widgets.letter_button_frame.letter_button_frame import LetterButtonFrame


class LetterButtonManager:
    def __init__(self, letter_button_frame: "LetterButtonFrame") -> None:
        self.letter_rows = letter_button_frame.letter_rows
        self.icon_dir = LETTER_BTN_ICON_DIR
        self.buttons: Dict[Letters, LetterButton] = {}
        self.letter_button_frame = letter_button_frame
        self.click_handler = LetterButtonClickHandler(self)

    def create_buttons(self) -> None:
        for type_name, rows in self.letter_rows.items():
            for row in rows:
                for letter_str in row:
                    letter_type = LetterType.get_letter_type(letter_str)
                    icon_path = f"{self.icon_dir}/{letter_type}/{letter_str}.svg"
                    button = self._create_letter_button(icon_path, letter_str)
                    self.buttons[letter_str] = button

    def _create_letter_button(self, icon_path: str, letter_str: str) -> LetterButton:
        button = LetterButton(icon_path, letter_str)
        LetterButtonStyler.apply_default_style(button)
        return button

    def resize_buttons(self, button_panel_height: int) -> None:
        button_row_count = sum(len(rows) for rows in self.letter_rows.values())
        button_size = int(button_panel_height / (button_row_count + 1))
        icon_size = int(button_size * 0.9)

        for button in self.buttons.values():
            button.setMinimumSize(QSize(button_size, button_size))
            button.setMaximumSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))

    def get_buttons_row_layout(self, row: List[Letters]) -> QHBoxLayout:
        row_layout = QHBoxLayout()
        row_layout.setSpacing(5)

        for letter_str in row:
            button = self.buttons[letter_str]
            row_layout.addWidget(button)

        # Don't add a stretch at the end of each row layout
        return row_layout

    def connect_letter_buttons(self) -> None:
        # Use the buttons from the manager to set up connections
        for letter, button in self.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: self.click_handler.on_letter_button_clicked(
                    letter
                )
            )
