from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
from utilities.TypeChecking.TypeChecking import Letters
from ..codex.codex_button_panel import CodexButtonPanel
from ..codex.codex_image_generator import CodexImageGenerator
from ..scroll_area.scroll_area import ScrollArea

if TYPE_CHECKING:
    from ..main_tab_widget.main_tab_widget import MainTabWidget


class Codex(QWidget):
    imageGenerated = pyqtSignal(str)
    selected_letters: List[Letters] = []

    def __init__(self, main_tab_widget: "MainTabWidget") -> None:
        super().__init__(main_tab_widget)
        self.main_tab_widget = main_tab_widget
        self.letters_dict = self.main_tab_widget.main_widget.letters

        self.scroll_area = ScrollArea(self)
        self.image_generator = CodexImageGenerator(self)
        self.button_panel = CodexButtonPanel(self)

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.scroll_area)
        self.right_layout.addWidget(self.button_panel)
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)

    def resize_codex(self) -> None:
        self.scroll_area.update_pictographs()
        self.button_panel.letter_btn_frame.resize_letter_button_frame()
