from Enums import LetterType
from typing import TYPE_CHECKING, Union

from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy
from PyQt6.QtCore import QSize, Qt
from Enums import LetterType
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
    from widgets.sequence_builder.components.sequence_builder_letter_button_frame import (
        SequenceBuilderLetterButtonFrame,
    )
    from widgets.letter_button_frame.codex_letter_button_frame import (
        CodexLetterButtonFrame,
    )


class LetterButtonManager:
    def __init__(
        self,
        letter_button_frame: Union[
            "CodexLetterButtonFrame", "SequenceBuilderLetterButtonFrame"
        ],
    ) -> None:
        self.letter_rows = letter_button_frame.letter_rows
        self.icon_dir = LETTER_BTN_ICON_DIR
        self.buttons: dict[Letters, LetterButton] = {}
        self.letter_button_frame = letter_button_frame
        self.click_handler = LetterButtonClickHandler(self)

    def create_buttons(self) -> None:
        for type_name, rows in self.letter_rows.items():
            for row in rows:
                for letter_str in row:
                    letter_type = LetterType.get_letter_type(letter_str)
                    icon_path = f"{self.icon_dir}/{letter_type.name}/{letter_str}.svg"
                    button = self._create_letter_button(icon_path, letter_str)
                    self.buttons[letter_str] = button

    def _create_letter_button(self, icon_path: str, letter_str: str) -> LetterButton:
        button = LetterButton(icon_path, letter_str)
        LetterButtonStyler.apply_default_style(button)
        return button

    def resize_buttons(self, button_panel_height: int) -> None:
        button_row_count = sum(len(rows) for rows in self.letter_rows.values())
        button_size = int((button_panel_height / (button_row_count)) * 0.8)
        icon_size = int(button_size * 0.9)

        for button in self.buttons.values():
            button.setMinimumSize(QSize(button_size, button_size))
            button.setMaximumSize(QSize(button_size, button_size))
            button.setIconSize(QSize(icon_size, icon_size))

    def get_buttons_row_layout(self, row: list[Letters]) -> QHBoxLayout:
        row_layout = QHBoxLayout()
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for letter_str in row:
            button = self.buttons[letter_str]
            button.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
            )  # Ensure buttons can expand
            row_layout.addWidget(button)
        return row_layout

    def connect_letter_buttons(self) -> None:
        for letter, button in self.buttons.items():
            button.clicked.connect(
                lambda checked, letter=letter: self.click_handler.on_letter_button_clicked(
                    letter
                )
            )
