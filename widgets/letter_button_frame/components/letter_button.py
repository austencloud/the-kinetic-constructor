from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor, QResizeEvent
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtSvg import QSvgRenderer
from Enums import LetterType
from constants import LETTER_BTN_ICON_DIR
from typing import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.TypeChecking import Letters

from utilities.TypeChecking.letter_lists import all_letters
from widgets.factories.letter_factory import LetterFactory


if TYPE_CHECKING:
    from widgets.codex.codex import Codex
    from widgets.main_widget.main_widget import MainWidget


class LetterButton(QPushButton):
    def __init__(self, icon_path: str, letter_str: str) -> None:
        super().__init__()
        self.setIcon(QIcon(icon_path))
        self.setFlat(True)
        self.setStyleSheet(self.get_button_style(False))
        self.letter = letter_str
        
    def get_button_style(self, pressed: bool) -> str:
        if pressed:
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """