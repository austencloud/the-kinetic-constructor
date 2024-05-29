from PyQt6.QtWidgets import QTabBar, QTabWidget
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class CustomTabBar(QTabBar):
    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.unsetCursor() 
        super().leaveEvent(event)
