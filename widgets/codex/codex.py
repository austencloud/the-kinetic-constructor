from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from utilities.TypeChecking.TypeChecking import Letters
from widgets.letter_button_frame.letter_button_frame import CodexLetterButtonFrame
from ..codex.codex_button_panel import CodexButtonPanel
from ..codex.codex_image_generator import CodexImageGenerator
from ..scroll_area.codex_scroll_area import CodexScrollArea

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Codex(QWidget):
    imageGenerated = pyqtSignal(str)
    selected_letters: list[Letters] = []

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.letters_dict = self.main_widget.letters

        self.scroll_area = CodexScrollArea(self)
        self.letter_button_frame = CodexLetterButtonFrame(self)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.scroll_area, 5)
        self.right_layout.addWidget(self.letter_button_frame, 1)
        self.layout.addLayout(self.left_layout, 5)
        self.layout.addLayout(self.right_layout, 1)

    def resize_codex(self) -> None:
        self.scroll_area.update_pictographs()
        self.letter_button_frame.resize_letter_button_frame()
