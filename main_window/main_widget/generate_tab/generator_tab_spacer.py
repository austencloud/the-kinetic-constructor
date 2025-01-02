from PyQt6.QtWidgets import (
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import QObject, pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class GeneratorTabSpacer(QSpacerItem):
    resized: pyqtSignal = pyqtSignal()

    def __init__(self, width: int, height: int):
        super().__init__(width, height, QSizePolicy.Policy.Minimum)
        self._height = height

    def resizeEvent(self, event):
        self.changeSize(0, self._height)
        self.resized.emit()
