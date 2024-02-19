from PyQt6.QtWidgets import QWidget
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.turns_box.codex_turns_box import CodexTurnsBox


class CodexWidget(QWidget):
    def __init__(self, turns_box) -> None:
        super().__init__(turns_box)
        self.turns_box: "CodexTurnsBox" = turns_box

