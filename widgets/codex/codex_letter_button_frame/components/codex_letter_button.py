from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    pass


class CodexLetterButton(QPushButton):
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

    def press(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=True))

    def release(self) -> None:
        self.setStyleSheet(self.get_button_style(pressed=False))

    def is_pressed(self) -> bool:
        return self.styleSheet() == self.get_button_style(pressed=True)
