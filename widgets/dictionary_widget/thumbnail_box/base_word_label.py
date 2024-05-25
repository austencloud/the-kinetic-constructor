from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class BaseWordLabel(QLabel):
    def __init__(self, base_word: str):
        super().__init__(base_word)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
