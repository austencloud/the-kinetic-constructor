from copy import deepcopy
from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QFrame,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from Enums import LetterType
from constants import CODEX_PICTOGRAPH
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.scroll_area import ScrollArea
from ..letter_button_frame.letter_button_frame import LetterButtonFrame

if TYPE_CHECKING:
    from widgets.codex.codex import Codex

class CodexImageGenerator:
    def __init__(self, codex: "Codex") -> None:
        self.codex = codex

    def generate_selected_images(self) -> None:
        main_widget = self.codex.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.codex.setMouseTracking(False)
        for letter in self.codex.selected_letters:
            pictograph_dict_list = self.codex.main_tab_widget.main_widget.letters[
                letter
            ]
            for pictograph_dict in pictograph_dict_list:
                codex_pictograph: Pictograph = (
                    self.codex.scroll_area.pictograph_factory.create_pictograph(
                        CODEX_PICTOGRAPH
                    )
                )
                codex_pictograph.image_renderer.render_and_cache_image()
        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.codex.setMouseTracking(True)

    def generate_all_images(self) -> None:
        main_widget = self.codex.parentWidget()
        main_widget.setEnabled(False)
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.codex.setMouseTracking(False)
        for (
            _,
            pictograph_dict_list,
        ) in self.codex.main_tab_widget.main_widget.letters.items():
            for pictograph_dict in pictograph_dict_list:
                codex_pictograph: Pictograph = (
                    self.codex.scroll_area.pictograph_factory.create_pictograph(
                        CODEX_PICTOGRAPH
                    )
                )
                codex_pictograph.image_renderer.render_and_cache_image()

        main_widget.setEnabled(True)
        QApplication.restoreOverrideCursor()
        self.codex.setMouseTracking(True)
