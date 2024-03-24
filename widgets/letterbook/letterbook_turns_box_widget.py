from PyQt6.QtWidgets import QWidget
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.letterbook.letterbook_letter_button_frame.components.letterbook_turns_box import (
        LetterBookTurnsBox,
    )


class LetterBookWidget(QWidget):
    def __init__(self, turns_box) -> None:
        super().__init__(turns_box)
        self.turns_box: "LetterBookTurnsBox" = turns_box
