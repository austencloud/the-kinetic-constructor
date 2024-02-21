from PyQt6.QtWidgets import QWidget
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.codex.codex_letter_button_frame.components.codex_turns_box import CodexTurnsBox


class CodexWidget(QWidget):
    def __init__(self, turns_box) -> None:
        super().__init__(turns_box)
        self.turns_box: "CodexTurnsBox" = turns_box


