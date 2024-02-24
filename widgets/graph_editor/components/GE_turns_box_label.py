from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QRect
from PyQt6.QtGui import QFont, QPainter, QIcon, QPixmap
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


class GE_TurnsBoxLabel(QLabel):
    clicked = pyqtSignal()  

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit() 
