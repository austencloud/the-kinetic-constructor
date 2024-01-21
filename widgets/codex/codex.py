from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from utilities.TypeChecking.TypeChecking import Letters
from widgets.codex.codex_button_panel import CodexButtonPanel
from widgets.codex.codex_image_generator import CodexImageGenerator
from widgets.scroll_area.scroll_area import ScrollArea


if TYPE_CHECKING:
    from widgets.main_tab_widget.main_tab_widget import MainTabWidget


class Codex(QWidget):
    imageGenerated = pyqtSignal(str)
    selected_letters: List[Letters] = []

    ### INITIALIZATION ###

    def __init__(self, main_tab_widget: "MainTabWidget") -> None:
        super().__init__(main_tab_widget)
        self.main_tab_widget = main_tab_widget
        self.letters_dict = self.main_tab_widget.main_widget.letters
        self._setup_layouts()
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        self.scroll_area = ScrollArea(self)
        self.image_generator = CodexImageGenerator(self)
        self.button_panel = CodexButtonPanel(self)
        self.left_layout.addWidget(self.scroll_area)
        self.right_layout.addWidget(self.button_panel)

    def _setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.right_layout)



    def toggle_pictograph_selection(self, state, index) -> None:
        if state == Qt.CheckState.Checked:
            self.selected_letters.append(index)
        else:
            self.selected_letters.remove(index)

    def update_letters_dict(self) -> None:
        for letter, pictograph_list in self.letters_dict.items():
            for pictograph_dict in pictograph_list:
                if "turns" in self.scroll_area.filter_tab_manager.filters:
                    pictograph_dict[
                        "blue_turns"
                    ] = self.scroll_area.filter_tab_manager.filters["turns"]

    def resize_codex(self) -> None:
        self.scroll_area.resize_scroll_area()
        self.scroll_area.update_pictographs()
        self.button_panel.letter_btn_frame.resize_letter_buttons()
