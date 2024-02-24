from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class GE_TurnsBoxLabel(QLabel):
    clicked = pyqtSignal()  

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit() 
